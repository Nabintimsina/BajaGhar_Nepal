import { Link, useLocation } from 'react-router-dom'
import { Music, Menu, X } from 'lucide-react'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useBranding } from '../context/BrandingContext'
import LanguageSwitcher from './LanguageSwitcher'
import './Navbar.css'

function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { branding } = useBranding()
  const { t } = useTranslation()
  const location = useLocation()

  const isActive = (path) => {
    return location.pathname === path ? 'active' : ''
  }

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  const closeMenu = () => {
    setIsMenuOpen(false)
  }

  return (
    <nav className="navbar">
      <div className="navbar-container container">
        <Link to="/" className="navbar-logo" onClick={closeMenu}>
          <span className="logo-mark" aria-hidden="true">
            {branding.logoUrl ? (
              <img className="logo-image" src={branding.logoUrl} alt={branding.logoAlt} />
            ) : (
              <Music className="logo-icon" aria-hidden="true" />
            )}
          </span>
          <span className="logo-text">{branding.name}</span>
        </Link>

        <button className="navbar-toggle" onClick={toggleMenu} aria-label={t('nav.toggleMenu')}>
          {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        <ul className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
          <li>
            <Link to="/" className={isActive('/')} onClick={closeMenu}>
              {t('nav.home')}
            </Link>
          </li>
          <li>
            <Link to="/instruments" className={isActive('/instruments')} onClick={closeMenu}>
              {t('nav.instruments')}
            </Link>
          </li>
          <li>
            <Link to="/learn" className={isActive('/learn')} onClick={closeMenu}>
              {t('nav.learn')}
            </Link>
          </li>
          <li>
            <Link to="/tuner" className={isActive('/tuner')} onClick={closeMenu}>
              {t('nav.tuner')}
            </Link>
          </li>
          <li>
            <Link to="/experts" className={isActive('/experts')} onClick={closeMenu}>
              {t('nav.experts')}
            </Link>
          </li>
          <li>
            <Link to="/about" className={isActive('/about')} onClick={closeMenu}>
              {t('nav.about')}
            </Link>
          </li>
          <li>
            <Link to="/contact" className={isActive('/contact')} onClick={closeMenu}>
              {t('nav.contact')}
            </Link>
          </li>
        </ul>
        <LanguageSwitcher />
      </div>
    </nav>
  )
}

export default Navbar
