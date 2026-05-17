import { Link } from 'react-router-dom'
import { Tag } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import './InstrumentCard.css'

function InstrumentCard({ instrument }) {
  const { t } = useTranslation()
  const { id, name, category, region, image, description } = instrument

  return (
    <div className="instrument-card card">
      <div className="instrument-card-image">
        <img src={image || '/placeholder-instrument.jpg'} alt={name} />
        <div className="instrument-card-overlay">
          <Tag size={16} />
          <span>{category}</span>
        </div>
      </div>
      <div className="instrument-card-content">
        <h3>{name}</h3>
        <p className="instrument-region">{region}</p>
        <p className="instrument-description">
          {description?.substring(0, 100)}...
        </p>
        <Link to={`/instruments/${id}`} className="btn btn-primary btn-small">
          {t('common.viewDetails')}
        </Link>
      </div>
    </div>
  )
}

export default InstrumentCard
