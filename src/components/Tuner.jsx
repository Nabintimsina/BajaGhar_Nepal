import { useState, useEffect, useRef } from 'react'
import { Mic, MicOff, Settings2, ChevronDown, ChevronUp } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { PitchDetector } from '../utils/pitchDetection'
import './Tuner.css'

function Tuner({ tunerConfig = null, defaultExpanded = true, compact = false }) {
  const { t } = useTranslation()
  const [isExpanded, setIsExpanded] = useState(defaultExpanded)
  const [isListening, setIsListening] = useState(false)
  const [frequency, setFrequency] = useState(null)
  const [closestNote, setClosestNote] = useState(null)
  const [error, setError] = useState('')
  const [permission, setPermission] = useState('pending')

  const audioContextRef = useRef(null)
  const pitchDetectorRef = useRef(null)
  const animationFrameRef = useRef(null)
  const streamRef = useRef(null)

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

  const getNoteAccuracy = (cents) => {
    const absCents = Math.abs(cents)
    if (absCents < 5) return 'excellent'
    if (absCents < 15) return 'good'
    if (absCents < 30) return 'needs-adjustment'
    return 'far'
  }

  const getListeningHint = () => {
    if (!isListening) return t('tuner.step1')
    if (!closestNote) return t('tuner.step2')
    if (Math.abs(closestNote.cents) < 5) return t('tuner.inTune')
    if (closestNote.cents > 0) return t('tuner.tooSharp')
    return t('tuner.tooFlat')
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

      const detectPitch = () => {
        const freq = pitchDetectorRef.current.getFrequency()

        if (freq > -1) {
          setFrequency(freq)

          const frequencyMap = getFrequencyMap()
          const closest = pitchDetectorRef.current.findClosestNote(freq, frequencyMap)
          setClosestNote(closest)
        } else {
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

    setIsListening(false)
    setFrequency(null)
    setClosestNote(null)
  }

  const getTuningStatus = () => {
    if (!closestNote) return 'waiting'
    if (Math.abs(closestNote.cents) < 5) return 'in-tune'
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
    // Convert cents to a 0-100 scale (±50 cents = 0-100)
    const cents = closestNote.cents
    return Math.max(0, Math.min(100, 50 + cents))
  }

  const tuningNotes = activeTuning.notes.map((note, idx) => ({
    note,
    frequency: activeTuning.frequencies[idx],
    index: idx,
  }))

  const tunerContent = (
    <div className="tuner-content tuner-content-compact">
      <div className="tuning-info">
        <div className="tuning-name-row">
          <p className="tuning-name">
          <strong>{t('tuner.tuning')}:</strong> {activeTuning.tuning_name}
          </p>
          <span className={`listening-pill ${isListening ? 'live' : ''}`}>
            {isListening ? t('tuner.listening') : t('tuner.startListening')}
          </span>
        </div>
        <div className="target-notes">
          <strong>{t('tuner.targetNotes')}:</strong>
          <span className="notes-list">
            {tuningNotes.map((item) => (
              <span
                key={item.index}
                className={`note-badge ${closestNote?.note === item.note ? 'active' : ''}`}
                title={`${item.note} • ${item.frequency.toFixed(2)} Hz`}
              >
                {item.note}
              </span>
            ))}
          </span>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
          {permission === 'denied' && (
            <p className="help-text">
              {t('tuner.allowMic')}
            </p>
          )}
        </div>
      )}

      {!error && (
        <div className="tuner-interface">
          <div className="frequency-display">
            {frequency ? (
              <>
                <div className="frequency-value">{frequency.toFixed(1)} Hz</div>
                {closestNote && (
                  <div className="note-info">
                    <div className={`note-name ${getTuningStatus()}`}>
                      {closestNote.note}
                    </div>
                    <div className="cent-diff">
                      {closestNote.cents > 0 ? '+' : ''}
                      {closestNote.cents.toFixed(1)} ¢
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="frequency-value waiting">--</div>
            )}
          </div>

          <div className={`live-readout ${getTuningStatus()}`}>
            <span>{getListeningHint()}</span>
            {closestNote && (
              <span className={`accuracy-badge ${getNoteAccuracy(closestNote.cents)}`}>
                {Math.abs(closestNote.cents).toFixed(1)} ¢ off
              </span>
            )}
          </div>

          <div className="tuning-meter">
            <div className="meter-label">
              <span>{t('tuner.flat')}</span>
              <span className={`status ${getTuningStatus()}`}>{getStatusMessage()}</span>
              <span>{t('tuner.sharp')}</span>
            </div>
            <div className="meter-bar">
              <div className="meter-scale">
                {[0, 25, 50, 75, 100].map((val) => (
                  <div key={val} className="scale-mark" style={{ left: `${val}%` }} />
                ))}
              </div>
              <div className="meter-fill">
                <div
                  className={`meter-needle ${getTuningStatus()}`}
                  style={{ left: `${getTuningBar()}%` }}
                />
              </div>
            </div>
          </div>

          <div className={`tuning-indicator ${getTuningStatus()}`}>
            <div className="indicator-dot" />
            <span>{getStatusMessage()}</span>
          </div>

          <button
            className={`mic-button ${isListening ? 'listening' : ''}`}
            onClick={isListening ? stopListening : startListening}
            aria-label={isListening ? t('tuner.stopListening') : t('tuner.startListening')}
          >
            {isListening ? (
              <>
                <MicOff size={24} />
                <span>{t('tuner.stopTuning')}</span>
              </>
            ) : (
              <>
                <Mic size={24} />
                <span>{t('tuner.startTuning')}</span>
              </>
            )}
          </button>

        </div>
      )}

      <div className="tuner-instructions">
        <h4>{t('tuner.howToUse')}</h4>
        <ul>
          <li>{t('tuner.step1')}</li>
          <li>{t('tuner.step2')}</li>
          <li>{t('tuner.step3')}</li>
          <li>{t('tuner.step4')}</li>
          <li>{t('tuner.step5')}</li>
        </ul>
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
