import { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../api/client'
import { useTranslation } from 'react-i18next'

const defaultBranding = {
  name: 'BAJAGHAR',
  logoUrl: '',
  logoAlt: 'BAJAGHAR logo',
  contactEmail: ''
}

const SITE_DESCRIPTION = 'Interactive digital learning platform for Traditional Musical Instruments of Nepal.'
const SITE_KEYWORDS = [
  'Nepal',
  'traditional musical instruments',
  'Nepali instruments',
  'Bajaghar',
  'culture',
  'music education',
  'नेपाल',
  'परम्परागत बाजा',
  'वाद्य यन्त्र',
  'baja nepal'
  
].join(', ')

const upsertMetaTag = (selector, attributes) => {
  let tag = document.head.querySelector(selector)
  if (!tag) {
    tag = document.createElement('meta')
    document.head.appendChild(tag)
  }

  Object.entries(attributes).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      tag.setAttribute(key, value)
    }
  })

  return tag
}

const BrandingContext = createContext({
  branding: defaultBranding,
  loading: true
})

export function BrandingProvider({ children }) {
  const [branding, setBranding] = useState(defaultBranding)
  const [loading, setLoading] = useState(true)
  const { i18n } = useTranslation()
  const activeLanguage = (i18n.resolvedLanguage || i18n.language || 'en').toLowerCase().startsWith('ne') ? 'ne' : 'en'

  useEffect(() => {
    let isMounted = true

    const loadBranding = async () => {
      if (isMounted) {
        setLoading(true)
      }

      try {
        const data = await api.get('branding/', { lang: activeLanguage })

        if (!isMounted || !data) {
          return
        }

        setBranding({
          name: data.name || defaultBranding.name,
          logoUrl: data.logo_url || '',
          logoAlt: data.logo_alt || `${data.name || defaultBranding.name} logo`,
          contactEmail: data.contact_email || ''
        })
      } catch {
        if (isMounted) {
          setBranding(defaultBranding)
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    loadBranding()

    return () => {
      isMounted = false
    }
  }, [activeLanguage])

  useEffect(() => {
    const title = branding.name || defaultBranding.name
    document.title = title

    upsertMetaTag('meta[name="description"]', {
      name: 'description',
      content: SITE_DESCRIPTION
    })

    upsertMetaTag('meta[name="keywords"]', {
      name: 'keywords',
      content: SITE_KEYWORDS
    })

    upsertMetaTag('meta[property="og:title"]', {
      property: 'og:title',
      content: title
    })

    upsertMetaTag('meta[property="og:description"]', {
      property: 'og:description',
      content: SITE_DESCRIPTION
    })

    upsertMetaTag('meta[property="og:type"]', {
      property: 'og:type',
      content: 'website'
    })

    upsertMetaTag('meta[property="og:site_name"]', {
      property: 'og:site_name',
      content: title
    })

    upsertMetaTag('meta[name="twitter:card"]', {
      name: 'twitter:card',
      content: 'summary_large_image'
    })

    upsertMetaTag('meta[name="twitter:title"]', {
      name: 'twitter:title',
      content: title
    })

    upsertMetaTag('meta[name="twitter:description"]', {
      name: 'twitter:description',
      content: SITE_DESCRIPTION
    })

    if (branding.logoUrl) {
      upsertMetaTag('meta[property="og:image"]', {
        property: 'og:image',
        content: branding.logoUrl
      })

      upsertMetaTag('meta[name="twitter:image"]', {
        name: 'twitter:image',
        content: branding.logoUrl
      })
    }

    const iconHref = branding.logoUrl || '/favicon.svg'
    let link = document.querySelector('link[rel~="icon"]')

    if (!link) {
      link = document.createElement('link')
      link.rel = 'icon'
      document.head.appendChild(link)
    }

    link.href = iconHref
  }, [branding])

  return <BrandingContext.Provider value={{ branding, loading }}>{children}</BrandingContext.Provider>
}

export function useBranding() {
  return useContext(BrandingContext)
}