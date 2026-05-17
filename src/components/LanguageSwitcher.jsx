import React, { useEffect, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import './LanguageSwitcher.css'

export default function LanguageSwitcher() {
  const { i18n, t } = useTranslation()
  const [isSwitching, setIsSwitching] = useState(false)
  const [switchingTo, setSwitchingTo] = useState(null)
  const timeoutRef = useRef(null)
  const activeLanguage = (i18n.resolvedLanguage || i18n.language || 'en').toLowerCase().startsWith('ne') ? 'ne' : 'en'

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        window.clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  useEffect(() => {
    const langCode = (i18n.resolvedLanguage || i18n.language || 'en')
    // keep html lang in sync so CSS targeting and number formatting locales work
    try {
      document.documentElement.lang = langCode
    } catch (e) {
      // noop
    }
  }, [i18n.resolvedLanguage, i18n.language])

  const handleLanguageChange = async (lang) => {
    if (lang === activeLanguage || isSwitching) {
      return
    }

    setIsSwitching(true)
    setSwitchingTo(lang)

    await i18n.changeLanguage(lang)
    localStorage.setItem('language', lang)
    localStorage.setItem('i18nextLng', lang)

    timeoutRef.current = window.setTimeout(() => {
      setIsSwitching(false)
      setSwitchingTo(null)
    }, 260)
  }

  return (
    <div className={`language-switcher ${isSwitching ? 'is-switching' : ''}`} aria-live="polite">
      <span className={`lang-indicator ${activeLanguage}`} aria-hidden="true" />
      <button
      
        className={`lang-btn ${activeLanguage === 'en' ? 'active' : ''} ${switchingTo === 'en' ? 'target' : ''}`}
        onClick={() => handleLanguageChange('en')}
        title={t('languageSwitcher.english')}
        disabled={isSwitching}
      >
        EN
      </button>
      <button
        className={`lang-btn ${activeLanguage === 'ne' ? 'active' : ''} ${switchingTo === 'ne' ? 'target' : ''}`}
        onClick={() => handleLanguageChange('ne')}
        title={t('languageSwitcher.nepali')}
        disabled={isSwitching}
      >
        नेप
      </button>
    </div>
  )
}
