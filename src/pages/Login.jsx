import { useState } from 'react'
import { Lock, Mail, Eye, EyeOff, AlertCircle, CheckCircle2, X } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import './Login.css'

function Login() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)
  const [isLogin, setIsLogin] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [showPopup, setShowPopup] = useState(false)
  const [popupMessage, setPopupMessage] = useState('')
  const [popupType, setPopupType] = useState('error') // 'error' or 'success'
  const [remainingSeconds, setRemainingSeconds] = useState(0)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    name: ''
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const showErrorPopup = (message, seconds = null) => {
    setPopupMessage(message)
    setPopupType('error')
    if (seconds) {
      setRemainingSeconds(seconds)
    }
    setShowPopup(true)
  }

  const showSuccessPopup = (message) => {
    setPopupMessage(message)
    setPopupType('success')
    setShowPopup(true)
    setTimeout(() => {
      setShowPopup(false)
      navigate('/admin/dashboard')
    }, 2000)
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const response = await fetch('/api/auth/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      })

      const data = await response.json()

      if (response.status === 429) {
        // Account locked
        showErrorPopup(
          data.detail || t('auth.accountLocked'),
          data.remaining_seconds
        )
      } else if (response.ok) {
        // Login successful
        localStorage.setItem('access_token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        showSuccessPopup(t('auth.loginSuccess'))
        setFormData({ username: '', password: '', confirmPassword: '', name: '' })
      } else {
        // Invalid credentials
        showErrorPopup(data.detail || t('auth.invalidCredentials'))
      }
    } catch (err) {
      showErrorPopup(t('auth.connectionError'))
      console.error('Login error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e) => {
    if (isLogin) {
      handleLogin(e)
    } else {
      e.preventDefault()
      // Registration not implemented yet
      showErrorPopup(t('auth.registrationNotAvailable'))
    }
  }

  const toggleMode = () => {
    setIsLogin(!isLogin)
    setFormData({
      username: '',
      password: '',
      confirmPassword: '',
      name: ''
    })
    setError('')
  }

  return (
    <div className="login-page">
      {showPopup && (
        <div className="contact-popup-overlay" role="presentation">
          <div
            className={`contact-popup contact-popup-${popupType}`}
            role={popupType === 'error' ? 'alert' : 'status'}
            aria-live="polite"
            aria-modal="true"
          >
            <button
              type="button"
              className="contact-popup-close"
              onClick={() => setShowPopup(false)}
              aria-label={t('contact.closePopup')}
            >
              <X size={18} />
            </button>
            <div className="contact-popup-icon">
              {popupType === 'error' ? <AlertCircle size={24} /> : <CheckCircle2 size={24} />}
            </div>
            <h3>{popupType === 'error' ? t('auth.error') : t('auth.success')}</h3>
            <p>{popupMessage}</p>
            {remainingSeconds > 0 && (
              <p style={{ fontSize: '0.9em', marginTop: '0.5rem', opacity: 0.8 }}>
                {t('auth.tryAgainIn')} {remainingSeconds} {t('auth.seconds')}
              </p>
            )}
          </div>
        </div>
      )}

      <div className="login-container">
        <div className="login-header">
          <Lock size={40} className="login-icon" />
          <h1>{isLogin ? t('auth.welcomeBack') : t('auth.createAccount')}</h1>
          <p>
            {isLogin 
              ? t('auth.loginPrompt') 
              : t('auth.registerPrompt')}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="name">{t('auth.fullName')}</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required={!isLogin}
                placeholder={t('auth.enterFullName')}
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">{isLogin ? t('auth.username') : t('auth.emailAddress')}</label>
            <div className="input-with-icon">
              <Mail size={20} className="input-icon" />
              <input
                type={isLogin ? 'text' : 'email'}
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                placeholder={isLogin ? t('auth.usernamePlaceholder') : t('auth.emailPlaceholder')}
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">{t('auth.password')}</label>
            <div className="input-with-icon">
              <Lock size={20} className="input-icon" />
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                placeholder={t('auth.passwordPlaceholder')}
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={t('auth.togglePasswordVisibility')}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="confirmPassword">{t('auth.confirmPassword')}</label>
              <div className="input-with-icon">
                <Lock size={20} className="input-icon" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required={!isLogin}
                  placeholder={t('auth.confirmPasswordPlaceholder')}
                />
              </div>
            </div>
          )}

          {isLogin && (
            <div className="form-options">
              <label className="remember-me">
                <input type="checkbox" />
                <span>{t('auth.rememberMe')}</span>
              </label>
              <a href="#forgot" className="forgot-link">{t('auth.forgotPassword')}</a>
            </div>
          )}

          {error && (
            <div className="error-message" style={{ color: '#c41e3a', fontSize: '0.9em' }}>
              {error}
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary btn-large login-button"
            disabled={isLoading}
          >
            {isLoading ? t('auth.loggingIn') : (isLogin ? t('auth.logIn') : t('auth.signUp'))}
          </button>
        </form>

        <div className="login-divider">
          <span>{t('auth.or')}</span>
        </div>

        <div className="social-login">
          <button className="social-button google-button" disabled>
            <svg width="20" height="20" viewBox="0 0 20 20">
              <path fill="#4285F4" d="M19.6 10.2c0-.7-.1-1.4-.2-2H10v3.8h5.4c-.2 1.2-1 2.3-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z"/>
              <path fill="#34A853" d="M10 20c2.7 0 4.9-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.2H1.1v2.6C2.8 17.8 6.1 20 10 20z"/>
              <path fill="#FBBC05" d="M4.4 11.9c-.4-1.2-.4-2.5 0-3.7V5.6H1.1c-1.4 2.8-1.4 6.1 0 8.9l3.3-2.6z"/>
              <path fill="#EA4335" d="M10 3.9c1.5 0 2.8.5 3.8 1.5l2.8-2.8C14.9.9 12.7 0 10 0 6.1 0 2.8 2.2 1.1 5.6l3.3 2.6C5.2 5.7 7.4 3.9 10 3.9z"/>
            </svg>
            {t('auth.continueWithGoogle')}
          </button>
        </div>

        <div className="login-footer">
          <p>
            {isLogin ? t('auth.dontHaveAccount') : t('auth.alreadyHaveAccount')}
            {' '}
            <button className="toggle-mode-button" onClick={toggleMode}>
              {isLogin ? t('auth.signUp') : t('auth.logIn')}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login

