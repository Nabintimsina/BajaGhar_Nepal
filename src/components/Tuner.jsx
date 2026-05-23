import { useState, useEffect, useRef } from 'react'
import { Mic, MicOff, Settings2, ChevronDown, ChevronUp } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { PitchDetector } from '../utils/pitchDetection'
import SarangiDisplay from './SarangiDisplay'
import './Tuner.css'

function Tuner({ tunerConfig = null, defaultExpanded = true, compact = false, instrumentName = '' }) {
  const { t } = useTranslation()
  const [isExpanded, setIsExpanded] = useState(defaultExpanded)
  const [isListening, setIsListening] = useState(false)
  const [frequency, setFrequency] = useState(null)
  const [closestNote, setClosestNote] = useState(null)
  const [error, setError] = useState('')
  const [permission, setPermission] = useState('pending')
  const [isHoldActive, setIsHoldActive] = useState(false)

  const audioContextRef = useRef(null)
  const pitchDetectorRef = useRef(null)
  const animationFrameRef = useRef(null)
  const streamRef = useRef(null)
  const stabilityRef = useRef({ note: null, stableFrames: 0, lastFrequency: null })
  const holdUntilRef = useRef(0)
  const lastDetectedAtRef = useRef(0)

  const IN_TUNE_CENTS = 7
  const ACCEPTABLE_CENTS_WINDOW = 100
  const REQUIRED_STABLE_FRAMES = 6
  const HOLD_MS = 1200
  const SIGNAL_HOLD_MS = 900
  const MAX_FREQ_JUMP_RATIO = 0.10
  const METER_CENT_RANGE = 50
  const ALLOWED_SEMITONE_DISTANCE = 2

  // Default tuning (Guitar standard)
  const defaultTuning = {
    tuning_name: t('tuner.defaultTuningName'),
    notes: ['E2', 'A2', 'D3', 'G3', 'B3', 'E4'],
    frequencies: [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]
  }

  const activeTuning = tunerConfig || defaultTuning

  useEffect(() => {
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop())
      }

      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        audioContextRef.current.close().catch(() => {})
      }
    }
  }, [])

  // Frequency-note mapping
  const getFrequencyMap = () => {
    return activeTuning.frequencies.map((freq, idx) => ({
      note: activeTuning.notes[idx],
      frequency: freq
    }))
  }

  const getSemitoneDistance = (freq1, freq2) => {
    return 12 * Math.log2(freq1 / freq2)
  }

  const isWithinSemitoneRange = (freq, targetFreq) => {
    const distance = Math.abs(getSemitoneDistance(freq, targetFreq))
    return distance <= ALLOWED_SEMITONE_DISTANCE
  }

  const getNoteAccuracy = (cents) => {
    const absCents = Math.abs(cents)
    if (absCents < IN_TUNE_CENTS) return 'excellent'
    if (absCents < 8) return 'good'
    if (absCents < 15) return 'needs-adjustment'
    return 'far'
  }

  const getListeningHint = () => {
    if (!isListening) return t('tuner.step1')
    if (!closestNote) return t('tuner.step2')
    if (isHoldActive) return `${t('tuner.inTune')} (hold)`
    if (Math.abs(closestNote.cents) < IN_TUNE_CENTS) return t('tuner.inTune')
    if (closestNote.cents > 0) return t('tuner.tooSharp')
    return t('tuner.tooFlat')
  }

  const resetTrackingState = (clearReadout = false) => {
    stabilityRef.current = { note: null, stableFrames: 0, lastFrequency: null }
    holdUntilRef.current = 0
    lastDetectedAtRef.current = 0
    setIsHoldActive(false)

    if (clearReadout) {
      setFrequency(null)
      setClosestNote(null)
    }
  }

  const startListening = async () => {
    try {
      setError('')

      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      }

      // Some browsers require a user gesture to resume the audio context
      if (audioContextRef.current.state === 'suspended') {
        try {
          await audioContextRef.current.resume()
        } catch (e) {
          // ignore resume errors
        }
      }

      if (!pitchDetectorRef.current) {
        pitchDetectorRef.current = new PitchDetector(audioContextRef.current)
      }

      const stream = await pitchDetectorRef.current.setupMicrophone()
      streamRef.current = stream
      setPermission('granted')
      setIsListening(true)
      resetTrackingState(true)

      const detectPitch = () => {
        const now = Date.now()

        if (holdUntilRef.current > now) {
          setIsHoldActive(true)
          animationFrameRef.current = requestAnimationFrame(detectPitch)
          return
        }

        if (holdUntilRef.current !== 0) {
          holdUntilRef.current = 0
          setIsHoldActive(false)
        }

        const freq = pitchDetectorRef.current.getFrequency()

        if (freq > -1) {
          const frequencyMap = getFrequencyMap()
          const closest = pitchDetectorRef.current.findClosestNote(freq, frequencyMap)

          const isInSemitoneRange = activeTuning.frequencies.some((targetFreq) =>
            isWithinSemitoneRange(freq, targetFreq)
          )

          if (!closest || !isInSemitoneRange) {
            stabilityRef.current = { note: null, stableFrames: 0, lastFrequency: null }
            animationFrameRef.current = requestAnimationFrame(detectPitch)
            return
          }

          if (closest && Math.abs(closest.cents) <= ACCEPTABLE_CENTS_WINDOW) {
            const stability = stabilityRef.current
            const sameNote = stability.note === closest.note
            const jumpRatio = stability.lastFrequency
              ? Math.abs(freq - stability.lastFrequency) / closest.frequency
              : 0
            const smoothTransition = jumpRatio <= MAX_FREQ_JUMP_RATIO

            if (sameNote && smoothTransition) {
              stability.stableFrames += 1
            } else {
              stability.note = closest.note
              stability.stableFrames = 1
            }

            stability.lastFrequency = freq

            if (stability.stableFrames >= REQUIRED_STABLE_FRAMES) {
              setFrequency(freq)
              setClosestNote(closest)
              lastDetectedAtRef.current = now

              if (Math.abs(closest.cents) <= IN_TUNE_CENTS) {
                holdUntilRef.current = now + HOLD_MS
                setIsHoldActive(true)
              }
            }
          } else {
            stabilityRef.current = { note: null, stableFrames: 0, lastFrequency: null }
          }
        } else {
          stabilityRef.current = { note: null, stableFrames: 0, lastFrequency: null }
        }

        if (lastDetectedAtRef.current && now - lastDetectedAtRef.current > SIGNAL_HOLD_MS) {
          setFrequency(null)
          setClosestNote(null)
        }

        animationFrameRef.current = requestAnimationFrame(detectPitch)
      }

      animationFrameRef.current = requestAnimationFrame(detectPitch)
    } catch (err) {
      // Better messaging for common getUserMedia errors
      if (err && err.name === 'NotAllowedError') {
        setError(t('tuner.micBlocked'))
        setPermission('denied')
      } else if (err && err.name === 'NotFoundError') {
        setError(t('tuner.noMic'))
      } else {
        setError(err.message || String(err))
      }

      setIsListening(false)
    }
  }

  const stopListening = () => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current)
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
    }

    resetTrackingState()
    setIsListening(false)
    setFrequency(null)
    setClosestNote(null)
  }

  const getTuningStatus = () => {
    if (!closestNote) return 'waiting'
    if (Math.abs(closestNote.cents) < IN_TUNE_CENTS) return 'in-tune'
    if (closestNote.cents > 0) return 'sharp'
    return 'flat'
  }

  const getStatusMessage = () => {
    const status = getTuningStatus()
    if (status === 'waiting') return t('tuner.listening')
    if (status === 'in-tune') return t('tuner.inTune')
    if (status === 'sharp') return t('tuner.tooSharp')
    return t('tuner.tooFlat')
  }

  const getTuningBar = () => {
    if (!closestNote) return 0
    // Keep the meter focused around a tighter band for precise tuning.
    const cents = Math.max(-METER_CENT_RANGE, Math.min(METER_CENT_RANGE, closestNote.cents))
    return Math.max(0, Math.min(100, 50 + (cents / METER_CENT_RANGE) * 50))
  }

  const tuningNotes = activeTuning.notes.map((note, idx) => ({
    note,
    frequency: activeTuning.frequencies[idx],
    index: idx,
  }))

















  

  // current string indicator removed — only tuning meter is shown

  const tunerContent = (
    <div className="tuner-content tuner-content-compact">
      {error && (
        <div className="error-message">
          <p>{error}</p>
          {permission === 'denied' && (
            <p className="help-text">{t('tuner.allowMic')}</p>
          )}
        </div>
      )}

      <div className="tuner-interface">
        <div className="tuning-display-container">
          {/* Target notes based on selected tuning standard */}
          <div className="tuning-info">
            <div className="target-notes">
              <strong>{t('tuner.targetNotes')}:</strong>
              <span className="notes-list">
                {activeTuning.notes.map((note, idx) => (
                  <span
                    key={note}
                    className={`note-badge ${closestNote?.note === note ? 'active' : ''}`}
                    title={note}
                  >
                    {note}
                  </span>
                ))}
              </span>
            </div>
          </div>

          <div className="tuning-display-main">
            {/* Top: Combined tuning meter + status */}
            <div className={`tuning-top ${getTuningStatus()}`}>
              <div className={`tuning-meter ${getTuningStatus()}`}>
                <div className="tuning-note">{closestNote?.note || '--'}</div>
                <div className="tuning-cents">{closestNote ? `${closestNote.cents > 0 ? '+' : ''}${closestNote.cents.toFixed(1)}¢` : '--'}</div>
                {/* tuning-string-label removed; only tuning-meter remains */}
                <div className="tuning-status-message">
                  {getTuningStatus() === 'in-tune' && <span className="status-in-tune">✓ {t('tuner.inTune')}</span>}
                  {getTuningStatus() === 'sharp' && <span className="status-sharp">↑ {t('tuner.tooSharp')}</span>}
                  {getTuningStatus() === 'flat' && <span className="status-flat">↓ {t('tuner.tooFlat')}</span>}
                  {getTuningStatus() === 'waiting' && isListening && <span className="status-listening">🎵 {t('tuner.listening')}</span>}
                </div>
              </div>

              {/* status-display removed — only tuning-meter shows status now */}
            </div>

            {/* Sarangi Display */}
            {activeTuning.notes.length === 4 && (
              <SarangiDisplay
                closestNote={closestNote}
                frequency={frequency}
                tuningStatus={getTuningStatus()}
                activeTuning={activeTuning}
              />
            )}
          </div>
        </div>

        {/* Centered mic button across the page */}
        <div className="mic-center">
          <button
            className={`mic-button ${isListening ? 'listening' : ''}`}
            onClick={isListening ? stopListening : startListening}
            aria-label={isListening ? t('tuner.stopListening') : t('tuner.startListening')}
          >
            {isListening ? (
              <>
                <Mic size={18} />
                <span className="sr-only">{t('tuner.stopListening')}</span>
              </>
            ) : (
              <>
                <MicOff size={18} />
                <span className="sr-only">{t('tuner.startListening')}</span>
              </>
            )}
          </button>
        </div>

        {activeTuning.instructions && (
          <div className="tuning-instructions">
            <div className="tuning-instructions-title">{t('tuner.tuningTips')}</div>
            <p>{activeTuning.instructions}</p>
          </div>
        )}
      </div>
    </div>
  )

  if (compact) {
    return <div className="tuner-compact">{tunerContent}</div>
  }

  return (
    <section className="section tuner-section">
      <div className="container">
        <div className="tuner-header" onClick={() => setIsExpanded(!isExpanded)}>
          <h2 className="section-title">
            <Settings2 size={24} />
            {t('learn.tuner')}
          </h2>
          <button className="expand-btn" aria-label="Toggle tuner">
            {isExpanded ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
          </button>
        </div>

        {isExpanded && tunerContent}
      </div>
    </section>
  )
}

export default Tuner
