import { useState } from 'react'
import logo from './assets/logo.png'
import './index.css'

function App() {
  return (
    <div className="app-container">
      {/* Hero Section */}
      <section className="hero-section">
        <img src={logo} className="logo" alt="Patio PTY Logo" />
        <h1>PATIO PTY</h1>
        <p className="subtitle">Privacidad Absoluta. Planes Reales.</p>
        
        <div className="glass-card">
          <p style={{ fontSize: '1.2rem', marginBottom: '1.5rem' }}>
            La primera comunidad de citas en Panamá diseñada para quienes valoran la discreción y las conexiones de calidad.
          </p>
          <button className="cta-button">Solicitar Invitación</button>
        </div>
      </section>

      {/* Features Grid */}
      <div className="features-grid">
        <div className="feature-item glass-card">
          <h3>🔐 Privacidad Progresiva</h3>
          <p>Tú controlas quién ve tus fotos y cuándo. Tu identidad es tu activo más valioso.</p>
        </div>
        
        <div className="feature-item glass-card">
          <h3>📍 Citas por Planes</h3>
          <p>Menos swipe, más acción. Propón un plan (Cena, Rooftop, Parking) y conecta con alguien que quiera lo mismo.</p>
        </div>

        <div className="feature-item glass-card">
          <h3>⚡ Descubrimiento en Vivo</h3>
          <p>Modo espontáneo para conocer gente real en tiempo real, con verificación de seguridad obligatoria.</p>
        </div>
      </div>

      {/* Popular Plans Section */}
      <h2 style={{ marginTop: '4rem', fontSize: '2rem', color: 'var(--primary)' }}>Planes Populares hoy en PTY</h2>
      <div className="features-grid" style={{ marginTop: '2rem' }}>
        <div className="feature-item glass-card" style={{ textAlign: 'left', borderLeft: '4px solid var(--primary)' }}>
          <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>GASTRONOMÍA</span>
          <h4 style={{ margin: '0.5rem 0' }}>Cena en San Francisco</h4>
          <p>3 personas buscando este plan ahora mismo.</p>
        </div>
        <div className="feature-item glass-card" style={{ textAlign: 'left', borderLeft: '4px solid var(--secondary)' }}>
          <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>NIGHTLIFE</span>
          <h4 style={{ margin: '0.5rem 0' }}>Parking en Casco Viejo</h4>
          <p>Descubre quién está en el rooftop hoy.</p>
        </div>
        <div className="feature-item glass-card" style={{ textAlign: 'left', borderLeft: '4px solid var(--primary)' }}>
          <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>OUTDOOR</span>
          <h4 style={{ margin: '0.5rem 0' }}>Sunset en el Causeway</h4>
          <p>Ideal para una primera conexión relajada.</p>
        </div>
      </div>

      {/* Social / Footer (Simplified for MVP) */}
      <footer style={{ marginTop: 'auto', padding: '2rem', textAlign: 'center', opacity: 0.6 }}>
        <p>© 2026 Patio PTY - El Salvador de tu vida social.</p>
      </footer>
    </div>
  )
}

export default App
