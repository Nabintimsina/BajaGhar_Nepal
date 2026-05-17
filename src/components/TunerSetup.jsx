import { useState } from 'react'
import { api } from '../api/client'
import './Tuner.css'

function TunerSetup({ instrumentId, onCreated }) {
  const [tuningName, setTuningName] = useState('Standard')
  const [notes, setNotes] = useState('E2,A2,D3,G3,B3,E4')
  const [frequencies, setFrequencies] = useState('82.41,110.00,146.83,196.00,246.94,329.63')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleCreate = async () => {
    setLoading(true)
    setError('')
    try {
      const notesArr = notes.split(',').map((s) => s.trim()).filter(Boolean)
      const freqs = frequencies.split(',').map((s) => parseFloat(s)).filter((n) => !Number.isNaN(n))

      await api.post('tuner-configurations/', {
        instrument: instrumentId,
        tuning_name: tuningName,
        notes: notesArr,
        frequencies: freqs,
        is_default: false,
      })

      if (onCreated) await onCreated()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="tuner-setup-form">
      {error && <p className="error">{error}</p>}
      <div>
        <label>Tuning name</label>
        <input value={tuningName} onChange={(e) => setTuningName(e.target.value)} />
      </div>
      <div>
        <label>Notes (comma separated)</label>
        <input value={notes} onChange={(e) => setNotes(e.target.value)} />
      </div>
      <div>
        <label>Frequencies (Hz, comma separated)</label>
        <input value={frequencies} onChange={(e) => setFrequencies(e.target.value)} />
      </div>
      <div style={{ marginTop: 8 }}>
        <button className="btn btn-primary" onClick={handleCreate} disabled={loading}>
          {loading ? 'Creating...' : 'Create tuner configuration'}
        </button>
      </div>
    </div>
  )
}

export default TunerSetup
