import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, MapPin, Tag } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import Viewer3D from '../components/Viewer3D'
import VideoTutorial from '../components/VideoTutorial'
import { api } from '../api/client'
import './InstrumentDetail.css'

function InstrumentDetail() {
  const { t, i18n } = useTranslation()
  const activeLanguage = (i18n.resolvedLanguage || i18n.language || 'en').toLowerCase().startsWith('ne') ? 'ne' : 'en'
  const { id } = useParams()
  const [instrument, setInstrument] = useState(null)
  const [tutorials, setTutorials] = useState([])
  const [expandedSections, setExpandedSections] = useState({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [id])

  useEffect(() => {
    setExpandedSections({})
  }, [id])

  useEffect(() => {
    let isMounted = true

    const loadInstrument = async () => {
      setIsLoading(true)
      setError('')

      try {
        const response = await api.get(`instruments/${id}/`, { lang: activeLanguage })
        if (isMounted) setInstrument(response)

        try {
          const tutorialsData = await api.get(`instruments/${id}/tutorials/`, { lang: activeLanguage })
          if (isMounted) setTutorials(tutorialsData || [])
        } catch {
          if (isMounted) setTutorials([])
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message)
          setInstrument(null)
        }
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    loadInstrument()

    return () => {
      isMounted = false
    }
  }, [id, activeLanguage])

  if (isLoading) {
    return (
      <div className="container instrument-state">
        <h2>{t('instrumentDetail.loading')}</h2>
      </div>
    )
  }

  if (error || !instrument) {
    return (
      <div className="container instrument-state">
        <h2>{t('instrumentDetail.notFound')}</h2>
        {error && <p>{error}</p>}
        <Link to="/instruments" className="btn btn-primary">
          {t('instrumentDetail.backToInstruments')}
        </Link>
      </div>
    )
  }

  const relatedExperts = instrument.experts || []
  const instructorProfiles = relatedExperts.reduce((map, expert) => {
    if (expert?.name) {
      map[expert.name.trim().toLowerCase()] = expert.id
    }
    return map
  }, {})
  const heroDescription = instrument.description || t('instrumentDetail.notSpecified')

  const renderSectionText = (value) => value || t('instrumentDetail.notSpecified')
  const sectionPreviewLimit = 220

  const renderExpandableSection = (sectionKey, value) => {
    const text = renderSectionText(value)
    const isLong = text.length > sectionPreviewLimit
    const isExpanded = expandedSections[sectionKey] ?? false
    const needsPreview = isLong && !isExpanded

    return (
      <>
        <p className={`content-text ${needsPreview ? 'content-text-clamped' : ''}`}>
          {text}
        </p>
        {isLong && (
          <button
            type="button"
            className="content-toggle"
            onClick={() => setExpandedSections((current) => ({ ...current, [sectionKey]: !current[sectionKey] }))}
          >
            {isExpanded ? t('instrumentDetail.seeLess') : t('instrumentDetail.seeMore')}
          </button>
        )}
      </>
    )
  }

  return (
    <div className="instrument-detail-page">
      <section className="instrument-hero">
        <div className="container">
          <Link to="/instruments" className="back-link">
            <ArrowLeft size={20} />
            {t('instrumentDetail.backToInstruments')}
          </Link>

          <div className="instrument-hero-grid">
            <div className="instrument-hero-copy">
              <div className="header-badges">
                <span className="badge badge-category">
                  <Tag size={16} />
                  {instrument.category}
                </span>
                <span className="badge badge-region">
                  <MapPin size={16} />
                  {instrument.region}
                </span>
              </div>

              <h1>{instrument.name}</h1>
              <p className="instrument-intro">{heroDescription}</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section instrument-main-section">
        <div className="container">
          <div className="instrument-layout">
            <div className="media-grid">
              <article className="detail-box">
                <div className="section-heading section-heading-tight">
                  <span className="eyebrow">{t('instrumentDetail.interactiveModel')}</span>
                  <h2>{t('instrumentDetail.modelViewer')}</h2>
                </div>
                <div className="media-panel">
                  <Viewer3D
                    modelSrc={instrument.model_3d}
                    title={instrument.name}
                    showBrightnessControl={Boolean(instrument.show_brightness_control)}
                  />
                </div>
              </article>

              <article className="detail-box">
                <div className="section-heading section-heading-tight">
                  <span className="eyebrow">{t('instrumentDetail.watchAndLearn')}</span>
                  <h2>{t('learn.tutorials')}</h2>
                </div>
                <div className="media-panel">
                  {tutorials.length > 0 ? (
                    <VideoTutorial tutorials={tutorials} compact instructorProfiles={instructorProfiles} />
                  ) : (
                    <div className="empty-media-state">
                      <p>{t('instrumentDetail.noTutorials')}</p>
                    </div>
                  )}
                </div>
              </article>
            </div>

            <div className="content-grid">
              <article className="detail-box content-box content-card content-card-history">
                <div className="section-heading section-heading-tight">
                  <h2>{t('instrumentDetail.history')}</h2>
                </div>
                {renderExpandableSection('history', instrument.history)}
              </article>

              <article className="detail-box content-box content-card content-card-materials">
                <div className="section-heading section-heading-tight">
                  <h2>{t('instrumentDetail.materials')}</h2>
                </div>
                {renderExpandableSection('materials', instrument.materials)}
              </article>

              <article className="detail-box content-box content-card content-card-playing">
                <div className="section-heading section-heading-tight">
                  <h2>{t('instrumentDetail.playingTechniques')}</h2>
                </div>
                {renderExpandableSection('playing', instrument.playing_technique)}
              </article>

              <article className="detail-box content-box content-card content-card-cultural">
                <div className="section-heading section-heading-tight">
                  <h2>{t('instrumentDetail.culturalSignificance')}</h2>
                </div>
                {renderExpandableSection('cultural', instrument.cultural_significance)}
              </article>
            </div>

          </div>
        </div>
      </section>

      <section className="section related-section bg-secondary">
        <div className="container">
          <h2 className="section-title">{t('instrumentDetail.exploreMore')}</h2>
          <div className="related-links">
            <Link to="/instruments" className="btn btn-primary">
              {t('instrumentDetail.viewAllInstruments')}
            </Link>
            <Link to="/tuner" className="btn btn-secondary">
              {t('learn.tuner')}
            </Link>
            <Link to="/learn" className="btn btn-secondary">
              {t('instrumentDetail.continueLearning')}
            </Link>
          </div>
        </div>
      </section>

      <section className="section instrument-acknowledgments">
        <div className="container">
          <div className="acknowledgment-box">
            <h3>{t('instrumentDetail.sourcesAcknowledgmentsTitle')}</h3>
            <p>{t('instrumentDetail.sourcesAcknowledgmentsText')}</p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default InstrumentDetail