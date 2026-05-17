import { useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Building } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import './About.css'

function About() {
  const { t } = useTranslation()
  const location = useLocation()

  useEffect(() => {
    // Scroll to element if hash exists
    if (location.hash) {
      const elementId = location.hash.replace('#', '')
      const element = document.getElementById(elementId)
      if (element) {
        setTimeout(() => {
          element.scrollIntoView({ behavior: 'smooth' })
        }, 0)
      }
    } else {
      // Scroll to top if no hash
      window.scrollTo(0, 0)
    }
  }, [location])
  return (
    <div className="about-page">
      <div className="page-header">
        <div className="container">
          <h1>{t('about.title')}</h1>
          <p>{t('about.subtitle')}</p>
        </div>
      </div>

      {/* Introduction */}
      <section className="section intro-section">
        <div className="container">
          <div className="intro-content">
            <h2>{t('about.introduction')}</h2>
            <p>{t('about.introText')}</p>
          </div>
        </div>
      </section>

     


      {/* Development Team */}
      <section id="development-team" className="section development-team-section">
        <div className="container">
          <h2 className="section-title">{t('about.developmentTeam')}</h2>
          <div className="team-content">
            <p className="team-intro">{t('about.teamIntro')}</p>
            
            <div className="developers-list">
              <a href="https://www.linkedin.com/in/timsinanabin8/" target="_blank" rel="noopener noreferrer" className="developer-card">
                <h3>{t('about.developerName1')}</h3>
                <p className="developer-education">
                  {t('about.developerEducation')}<br/>
                  {t('about.developerCollege')}
                </p>
              </a>
              
              <a href="https://www.linkedin.com/in/yuttena-singh-dangol-1932a0325/" target="_blank" rel="noopener noreferrer" className="developer-card">
                <h3>{t('about.developerName2')}</h3>
                <p className="developer-education">
                  {t('about.developerEducation')}<br/>
                  {t('about.developerCollege')}
                </p>
              </a>
              
              <a href="https://www.linkedin.com/in/prepshuna-dhakal-129783335/" target="_blank" rel="noopener noreferrer" className="developer-card">
                <h3>{t('about.developerName3')}</h3>
                <p className="developer-education">
                  {t('about.developerEducation')}<br/>
                  {t('about.developerCollege')}
                </p>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="section cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>{t('about.joinMission')}</h2>
            <p>{t('about.joinMissionDesc')}</p>
            <div className="cta-buttons">
              <Link to="/contact" className="btn btn-secondary btn-large">
                {t('about.supportProject')}
              </Link>
              <Link to="/contact" className="btn btn-outline btn-large">
                {t('about.getInTouch')}
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default About
