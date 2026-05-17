import { useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { api } from '../api/client'
import './Learn.css'

function Learn() {
  const { t, i18n } = useTranslation()
  const activeLanguage = (i18n.resolvedLanguage || i18n.language || 'en').toLowerCase().startsWith('ne') ? 'ne' : 'en'
  const [topics, setTopics] = useState([])
  const [selectedTopic, setSelectedTopic] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  useEffect(() => {
    let isMounted = true

    const loadTopics = async () => {
      setIsLoading(true)
      setError('')
      try {
        const response = await api.get('learning/', { lang: activeLanguage })
        const items = Array.isArray(response) ? response : response?.results || []
        if (isMounted) {
          setTopics(items)
          setSelectedTopic(items[0] || null)
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message)
          setTopics([])
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadTopics()

    return () => {
      isMounted = false
    }
  }, [activeLanguage])

  const topicIndex = useMemo(() => {
    return topics.findIndex((topic) => topic.id === selectedTopic?.id)
  }, [topics, selectedTopic])

  return (
    <div className="learn-page">
      <div className="page-header">
        <div className="container">
          <h1>{t('learn.pageTitle')}</h1>
          <p>{t('learn.subtitle')}</p>
        </div>
      </div>

      <div className="learn-content container">
        {/* Left Topic List */}
        <aside className="topics-sidebar">
          <h3>{t('learn.topics')}</h3>
          {isLoading ? (
            <p>{t('learn.loading')}</p>
          ) : error ? (
            <p>{t('learn.loadError')} {error}</p>
          ) : (
            <nav className="topics-list">
              {topics.map(topic => (
                <button
                  key={topic.id}
                  className={`topic-item ${selectedTopic?.id === topic.id ? 'active' : ''}`}
                  onClick={() => setSelectedTopic(topic)}
                >
                  <span className="topic-number">{topic.order ?? topic.id}</span>
                  <span className="topic-title">{topic.title}</span>
                </button>
              ))}
            </nav>
          )}
        </aside>

        {/* Right Content Viewer */}
        <main className="content-viewer">
          {selectedTopic ? (
            <>
              <article className="content-article">
                <h2>{selectedTopic.title}</h2>
                <div 
                  className="content-body"
                  dangerouslySetInnerHTML={{ 
                    __html: selectedTopic.content
                      .replace(/\n\n/g, '</p><p>')
                      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
                  }}
                />
              </article>

              <div className="content-nav">
                {topicIndex > 0 && (
                  <button 
                    className="btn btn-primary"
                    onClick={() => setSelectedTopic(topics[topicIndex - 1])}
                  >
                    ← {t('learn.previousTopic')}
                  </button>
                )}
                {topicIndex < topics.length - 1 && (
                  <button 
                    className="btn btn-primary"
                    onClick={() => setSelectedTopic(topics[topicIndex + 1])}
                  >
                    {t('learn.nextTopic')} →
                  </button>
                )}
              </div>
            </>
          ) : (
            <div className="content-article">
              <h2>{t('learn.noLessons')}</h2>
              <p>{t('learn.noLessonsDesc')}</p>
            </div>
          )}

        </main>
      </div>
    </div>
  )
}

export default Learn
