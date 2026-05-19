import { useTranslation } from 'react-i18next'
import './SarangiDisplay.css'

function SarangiDisplay({ closestNote, frequency, tuningStatus, activeTuning }) {
  const { t } = useTranslation()

  // Map note to string info
  const stringNotes = activeTuning?.notes || ['G3', 'C4', 'G4', 'C5']
  const stringFrequencies = activeTuning?.frequencies || [196.00, 261.63, 392.00, 523.25]

  const strings = stringNotes.map((note, idx) => ({
    id: idx + 1,
    note,
    frequency: stringFrequencies[idx],
    position: idx,
  }))

  // Find current string being tuned
  const currentString = strings.find((str) => str.note === closestNote?.note)

  // Determine string status
  const getStringStatus = (str) => {
    if (currentString?.id === str.id) {
      if (tuningStatus === 'in-tune') return 'tuned'
      return 'tuning'
    }
    return 'not-started'
  }

  return (
    <div className="sarangi-display">

      {/* Sarangi Image with Interactive String Markers */}
      <div className="sarangi-container">
        <img src="/images/sarangi.png" alt="Sarangi" className="sarangi-image" />
        
        {/* String Labels - positioned on the strings themselves */}
        <div className="string-labels-overlay">
          {strings.map((str) => (
            <div
              key={`label-${str.id}`}
              className={`string-label-marker ${getStringStatus(str)}`}
              title={`String ${str.id}: ${str.note}`}
              aria-label={`String ${str.id} ${str.note}`}
            >
              <span className="string-label-text">{str.note}</span>
            </div>
          ))}
        </div>

        {/* Interactive String Overlay */}
        <div className="strings-overlay">
          {strings.map((str) => (
            <div
              key={str.id}
              className={`string-marker ${getStringStatus(str)}`}
              title={`String ${str.id}: ${str.note}`}
            >
              <div className={`string-peg ${getStringStatus(str)}`} aria-label={`Peg for string ${str.id} ${str.note}`} title={`Peg: ${str.note}`}>
                <span className="peg-number">{str.note}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* String status grid removed per request (tuner.tuningNotes) */}

      {/* Instructions removed per request */}
    </div>
  )
}

export default SarangiDisplay
