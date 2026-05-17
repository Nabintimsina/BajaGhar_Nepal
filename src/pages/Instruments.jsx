import { useEffect, useMemo, useState } from 'react'
import { Filter } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import InstrumentCard from '../components/InstrumentCard'
import { api } from '../api/client'
import './Instruments.css'

function Instruments() {
  const { t, i18n } = useTranslation()
  const activeLanguage = (i18n.resolvedLanguage || i18n.language || 'en').toLowerCase().startsWith('ne') ? 'ne' : 'en'
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedRegion, setSelectedRegion] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [categories, setCategories] = useState([{ slug: 'all', name: t('instruments.all') }])
  const [instruments, setInstruments] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  const regions = useMemo(() => {
    const uniqueRegions = Array.from(new Set(instruments.map((item) => item.region))).filter(Boolean)
    return [t('instruments.all'), ...uniqueRegions]
  }, [instruments, t])

  useEffect(() => {
    let isMounted = true

    const loadCategories = async () => {
      try {
        const response = await api.get('categories/', { lang: activeLanguage })
        const items = Array.isArray(response) ? response : response?.results || []
        if (isMounted && items.length > 0) {
          setCategories([{ slug: 'all', name: t('instruments.all') }, ...items])
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message)
        }
      }
    }

    loadCategories()

    return () => {
      isMounted = false
    }
  }, [activeLanguage, t])

  useEffect(() => {
    let isMounted = true

    const loadInstruments = async () => {
      setIsLoading(true)
      setError('')
      try {
        const response = await api.get('instruments/', {
          category: selectedCategory === 'all' ? undefined : selectedCategory,
          region: selectedRegion === 'all' ? undefined : selectedRegion,
          search: searchTerm.trim() || undefined,
          lang: activeLanguage
        })
        const items = Array.isArray(response) ? response : response?.results || []
        if (isMounted) {
          setInstruments(items)
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message)
          setInstruments([])
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadInstruments()

    return () => {
      isMounted = false
    }
  }, [selectedCategory, selectedRegion, searchTerm, activeLanguage])

  return (
    <div className="instruments-page">
      <div className="page-header">
        <div className="container">
          <h1>{t('instruments.pageTitle')}</h1>
          <p>{t('instruments.subtitle')}</p>
        </div>
      </div>

      <div className="instruments-content container">
        {/* Filter Panel */}
        <aside className="filter-panel">
          <div className="filter-header">
            <Filter size={20} />
            <h3>{t('instruments.filterTitle')}</h3>
          </div>

          <div className="filter-section">
            <h4>{t('instruments.search')}</h4>
            <input
              type="text"
              className="filter-search"
              placeholder={t('instruments.searchPlaceholder')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="filter-section">
            <h4>{t('instruments.category')}</h4>
            <select 
              className="filter-select"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              {categories.map(category => (
                <option key={category.slug} value={category.slug}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-section">
            <h4>{t('instruments.region')}</h4>
            <select 
              className="filter-select"
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value.toLowerCase())}
            >
              {regions.map(region => (
                <option key={region} value={region.toLowerCase()}>
                  {region}
                </option>
              ))}
            </select>
          </div>

          <button 
            className="btn btn-outline btn-small"
            onClick={() => {
              setSelectedCategory('all')
              setSelectedRegion('all')
              setSearchTerm('')
            }}
          >
            {t('instruments.clearFilters')}
          </button>
        </aside>

        {/* Instruments Grid */}
        <div className="instruments-grid-container">
          <div className="results-header">
            <h2>
              {activeLanguage === 'ne' ? String(instruments.length).replace(/[0-9]/g, d => '०१२३४५६७८९'[d]) : instruments.length} {instruments.length === 1 ? t('instruments.foundSingular') : t('instruments.foundPlural')}
            </h2>
          </div>

          {isLoading ? (
            <div className="no-results">
              <p>{t('instruments.loading')}</p>
            </div>
          ) : error ? (
            <div className="no-results">
              <p>{t('instruments.loadError')} {error}</p>
            </div>
          ) : instruments.length > 0 ? (
            <div className="grid grid-3 instruments-grid">
              {instruments.map(instrument => (
                <InstrumentCard key={instrument.id} instrument={instrument} />
              ))}
            </div>
          ) : (
            <div className="no-results">
              <p>{t('instruments.noResults')}</p>
              <button 
                className="btn btn-primary"
                onClick={() => {
                  setSelectedCategory('all')
                  setSelectedRegion('all')
                  setSearchTerm('')
                }}
              >
                {t('instruments.viewAllInstruments')}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Instruments
