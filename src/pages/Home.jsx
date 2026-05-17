import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Music, Users, Box, BookOpen } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import InstrumentCard from '../components/InstrumentCard'
import { api } from '../api/client'
import './Home.css'

function Home() {
  const { t, i18n } = useTranslation()
  const activeLanguage = (i18n.resolvedLanguage || i18n.language || 'en').toLowerCase().startsWith('ne') ? 'ne' : 'en'
  const [featuredInstruments, setFeaturedInstruments] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  useEffect(() => {
    let isMounted = true

    const mockFeaturedInstruments = [
      {
        id: 1,
        name: 'Sarangi',
        category: 'String',
        region: 'Western Nepal',
        image: '/images/instruments/sarangi.jpg',
        description: t('home.mockSarangiDesc'),
        model_3d: '/models/pillows.glb'
      },
      {
        id: 2,
        name: 'Madal',
        category: 'Percussion',
        region: 'Central Nepal',
        image: '/images/instruments/madal.jpg',
        description: t('home.mockMadalDesc'),
        model_3d: '/models/pillows.glb'
      },
      {
        id: 3,
        name: 'Bansuri',
        category: 'Wind',
        region: 'Southern Nepal',
        image: '/images/instruments/bansuri.jpg',
        description: t('home.mockBansuriDesc'),
        model_3d: '/models/flute.glb'
      }
    ]

    const loadFeatured = async () => {
      setIsLoading(true)
      setError('')
      try {
          const response = await api.get('instruments/', { is_featured: true, lang: activeLanguage })
        const items = Array.isArray(response) ? response : response?.results || []
        if (isMounted) {
          // Use API data if available, fallback to mock data
          setFeaturedInstruments(items.length > 0 ? items.slice(0, 6) : mockFeaturedInstruments)
        }
      } catch (err) {
        if (isMounted) {
          // Use mock data on API error
          setFeaturedInstruments(mockFeaturedInstruments)
          setError('')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadFeatured()

    return () => {
      isMounted = false
    }
  }, [activeLanguage, t])

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-overlay"></div>
        <div className="hero-content container">
          <h1 className="hero-title">{t('home.title')}</h1>
          <p className="hero-subtitle">
            {t('home.subtitle')}
          </p>
          <div className="hero-buttons">
            <Link to="/instruments" className="btn btn-primary btn-large">
              {t('home.explore')}
            </Link>
            <Link to="/about" className="btn btn-outline btn-large">
              {t('home.learnMore')}
            </Link>
          </div>
        </div>
      </section>

      {/* Why This Project Section */}
      <section className="section why-section bg-secondary">
        <div className="container">
          <h2 className="section-title">{t('home.whyProject')}</h2>
          <p className="section-subtitle">{t('home.whySubtitle')}</p>
          <div className="grid grid-4">
            <div className="feature-card">
              <div className="feature-icon">
                <Music size={40} />
              </div>
              <h3>{t('home.culturalPreservation')}</h3>
              <p>{t('home.culturalPreservationDesc')}</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <BookOpen size={40} />
              </div>
              <h3>{t('home.digitalLearning')}</h3>
              <p>{t('home.digitalLearningDesc')}</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <Box size={40} />
              </div>
              <h3>{t('home.threeD')}</h3>
              <p>{t('home.threeDDesc')}</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <Users size={40} />
              </div>
              <h3>{t('home.expertKnowledge')}</h3>
              <p>{t('home.expertKnowledgeDesc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Instruments Section */}
      <section className="section featured-section">
        <div className="container">
          <h2 className="section-title">{t('home.featured')}</h2>
          <p className="section-subtitle">{t('home.discoverInstruments')}</p>
          {isLoading ? (
            <div className="text-center">
              <p>{t('common.loading')}</p>
            </div>
          ) : error ? (
            <div className="text-center">
              <p>{t('common.error')}: {error}</p>
            </div>
          ) : (
            <div className="grid grid-3">
              {featuredInstruments.map(instrument => (
                <InstrumentCard key={instrument.id} instrument={instrument} />
              ))}
            </div>
          )}
          <div className="text-center mt-4">
            <Link to="/instruments" className="btn btn-secondary">
              {t('home.viewAll')}
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="section how-it-works bg-secondary">
        <div className="container">
          <h2 className="section-title">{t('home.howItWorks')}</h2>
          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <h3>{t('home.selectInstrument')}</h3>
              <p>{t('home.selectInstrumentDesc')}</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>{t('home.exploreThreeD')}</h3>
              <p>{t('home.exploreThreeDDesc')}</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>{t('home.learnFromExperts')}</h3>
              <p>{t('home.learnFromExpertsDesc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>{t('home.cta')}</h2>
            <p>{t('home.ctaDesc')}</p>
            <div className="cta-buttons">
              <Link to="/instruments" className="btn btn-secondary btn-large">
                {t('home.startExploring')}
              </Link>
              <Link to="/about" className="btn btn-outline btn-large">
                {t('home.aboutProject')}
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
