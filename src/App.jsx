import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Instruments from './pages/Instruments'
import InstrumentDetail from './pages/InstrumentDetail'
import Learn from './pages/Learn'
import TunerLab from './pages/TunerLab'
import Experts from './pages/Experts'
import ExpertDetail from './pages/ExpertDetail'
import About from './pages/About'
import Contact from './pages/Contact'
import Login from './pages/Login'
import ErrorPage from './pages/ErrorPage'
import { BrandingProvider } from './context/BrandingContext'
import './App.css'

function App() {
  const { i18n } = useTranslation()

  // Sync document language attribute with i18n language
  useEffect(() => {
    const language = i18n.language?.toLowerCase() || 'en'
    document.documentElement.lang = language.startsWith('ne') ? 'ne' : 'en'
    document.documentElement.dir = 'ltr' // Nepali uses left-to-right script
  }, [i18n.language])

  return (
    <Router>
      <BrandingProvider>
        <div className="app">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/instruments" element={<Instruments />} />
              <Route path="/instruments/:id" element={<InstrumentDetail />} />
              <Route path="/learn" element={<Learn />} />
              <Route path="/tuner" element={<TunerLab />} />
              <Route path="/experts" element={<Experts />} />
              <Route path="/experts/:id" element={<ExpertDetail />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/login" element={<Login />} />
              <Route path="*" element={<ErrorPage />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrandingProvider>
    </Router>
  )
}

export default App
