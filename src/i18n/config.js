import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import enTranslation from './locales/en.json'
import neTranslation from './locales/ne.json'

const resources = {
  en: {
    translation: enTranslation
  },
  ne: {
    translation: neTranslation
  }
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
      format: function(value, format, lng) {
        if (format === 'number') {
          try {
            const locale = lng && lng.toString().startsWith('ne') ? 'ne-NP-u-nu-deva' : 'en-US'
            return new Intl.NumberFormat(locale).format(value)
          } catch (e) {
            return value
          }
        }
        return value
      }
    }
  })

export default i18n

// Ensure document `lang` matches i18n on initial load so CSS font rules apply
if (typeof document !== 'undefined') {
  try {
    const langCode = (i18n.resolvedLanguage || i18n.language || 'en')
    document.documentElement.lang = langCode
  } catch (e) {
    // noop
  }
}
