// Pitch detection utility using Web Audio API
// Based on autocorrelation algorithm

export class PitchDetector {
  constructor(audioContext, bufferSize = 4096) {
    this.audioContext = audioContext
    this.bufferSize = bufferSize
    this.analyser = audioContext.createAnalyser()
    this.analyser.fftSize = bufferSize
    this.analyser.smoothingTimeConstant = 0.8
    this.dataArray = new Uint8Array(this.analyser.frequencyBinCount)
    this.buffer = new Float32Array(bufferSize)
    this.frequencyHistory = []
    this.maxHistory = 5
  }

  async setupMicrophone() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const source = this.audioContext.createMediaStreamSource(stream)
      // ensure analyser fftSize is a power of two and appropriate for buffer
      const fft = Math.pow(2, Math.ceil(Math.log2(this.bufferSize)))
      this.analyser.fftSize = Math.max(256, fft)
      source.connect(this.analyser)
      return stream
    } catch (error) {
      // re-throw original error so callers can inspect error.name
      throw error
    }
  }

  getFrequency() {
    this.analyser.getFloatTimeDomainData(this.buffer)
    const frequency = this.autoCorrelate(this.buffer, this.audioContext.sampleRate)

    if (frequency <= -1) {
      this.frequencyHistory = []
      return -1
    }

    this.frequencyHistory.push(frequency)
    if (this.frequencyHistory.length > this.maxHistory) {
      this.frequencyHistory.shift()
    }

    // Require persistent signal for a short duration to reject transients.
    if (this.frequencyHistory.length < 2) {
      return -1
    }

    const sorted = [...this.frequencyHistory].sort((a, b) => a - b)
    return sorted[Math.floor(sorted.length / 2)]
  }

  autoCorrelate(buffer, sampleRate) {
    // Implements the autocorrelation algorithm for pitch detection
    // Returns frequency in Hz or -1 if not found

    let size = buffer.length
    let maxSamples = Math.floor(size / 2)
    let best_offset = -1
    let best_correlation = 0
    let rms = 0

    // Calculate RMS (root mean square) to check if there's enough signal
    for (let i = 0; i < size; i++) {
      let val = buffer[i]
      rms += val * val
    }
    rms = Math.sqrt(rms / size)

    // Not enough signal - need a minimum amplitude
    if (rms < 0.01) return -1

    // Find the best correlation offset
    let lastCorrelation = 1
    for (let offset = 1; offset < maxSamples; offset++) {
      let correlation = 0

      for (let i = 0; i < maxSamples; i++) {
        correlation += Math.abs(buffer[i] - buffer[i + offset])
      }

      correlation = 1 - correlation / maxSamples

      // Look for strong correlations that exceed previous ones
      if (correlation > 0.88 && correlation > lastCorrelation) {
        if (correlation > best_correlation) {
          best_correlation = correlation
          best_offset = offset
        }
      }

      lastCorrelation = correlation
    }

    // Return the frequency if we found a good correlation.
    if (best_offset > -1 && best_correlation > 0.88) {
      const frequency = sampleRate / best_offset
      // Keep detection within instrument-appropriate range.
      if (frequency < 60 || frequency > 1200) return -1
      return frequency
    }
    return -1
  }

  getNoteFromFrequency(frequency) {
    // A4 = 440 Hz reference
    const A4 = 440
    const C0 = A4 * Math.pow(2, -4.75)

    const halfStepsSinceC0 = 12 * Math.log2(frequency / C0)
    const octave = Math.floor(halfStepsSinceC0 / 12)
    const noteInOctave = Math.round(halfStepsSinceC0 % 12)

    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    const noteName = notes[noteInOctave]

    return {
      note: noteName + octave,
      cents: (halfStepsSinceC0 - Math.round(halfStepsSinceC0)) * 100
    }
  }

  findClosestNote(frequency, targetNotes) {
    let closestNote = null
    let minDifference = Infinity

    targetNotes.forEach((note) => {
      const difference = Math.abs(frequency - note.frequency)
      if (difference < minDifference) {
        minDifference = difference
        closestNote = {
          ...note,
          difference,
          cents: (12 * Math.log2(frequency / note.frequency)) * 100
        }
      }
    })

    return closestNote
  }
}

// Utility function to generate frequency chart data
export const getFrequencyChartData = (frequency, targetFrequencies) => {
  const frequencies = [
    { name: 'C2', freq: 65.41 },
    { name: 'D2', freq: 73.42 },
    { name: 'E2', freq: 82.41 },
    { name: 'F2', freq: 87.31 },
    { name: 'G2', freq: 98.00 },
    { name: 'A2', freq: 110.00 },
    { name: 'B2', freq: 123.47 },
    { name: 'C3', freq: 130.81 },
    { name: 'D3', freq: 146.83 },
    { name: 'E3', freq: 164.81 },
    { name: 'F3', freq: 174.61 },
    { name: 'G3', freq: 196.00 },
    { name: 'A3', freq: 220.00 },
    { name: 'B3', freq: 246.94 },
    { name: 'C4', freq: 261.63 },
    { name: 'D4', freq: 293.66 },
    { name: 'E4', freq: 329.63 },
    { name: 'F4', freq: 349.23 },
    { name: 'G4', freq: 392.00 },
    { name: 'A4', freq: 440.00 },
    { name: 'B4', freq: 493.88 },
    { name: 'C5', freq: 523.25 }
  ]

  return frequencies
}
