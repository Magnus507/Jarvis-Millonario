import React from 'react';
import { Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  Trophy, MapPin, QrCode, Zap, ChevronRight, 
  ShieldCheck, Lock, Mail, BarChart3, PlusCircle
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

// --- COMPONENTES DE UI REUTILIZABLES ---
const GlassCard = ({ children, className = "" }) => (
  <div className={`glass-card ${className}`}>
    {children}
  </div>
);

const InputField = ({ label, icon: Icon, type = "text", placeholder }) => (
  <div className="input-group">
    <label className="input-label">{label}</label>
    <div className="input-wrapper">
      <div className="input-icon">
        <Icon size={18} />
      </div>
      <input 
        type={type} 
        placeholder={placeholder}
        className="form-input"
      />
    </div>
  </div>
);

// --- VISTAS ---

const LandingView = () => {
  const navigate = useNavigate();
  return (
    <div className="container py-20 text-center">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <span className="neon-text mb-4" style={{display: 'block', fontWeight: 'bold', tracking: '0.1em', fontSize: '0.875rem'}}>PANAMÁ 2026</span>
        <h1 className="text-6xl mb-6">Cilindraje <span className="neon-text">507</span></h1>
        <p className="text-xl text-muted mx-auto mb-12" style={{maxWidth: '42rem'}}>
          El juego nacional donde tu moto es tu control. Escanea stickers, sube en el ranking y domina las provincias.
        </p>
        <div className="flex justify-center gap-4">
          <button onClick={() => navigate('/login')} className="btn btn-primary">
            Empezar el juego <ChevronRight size={20} />
          </button>
          <button onClick={() => navigate('/login')} className="btn btn-outline">
            Ingresar
          </button>
        </div>
      </motion.div>
    </div>
  );
};

const LoginView = () => {
  const navigate = useNavigate();
  return (
    <div className="container auth-container">
      <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="auth-card">
        <GlassCard>
          <div className="text-center mb-8">
            <h2 className="text-3xl mb-2">Bienvenido <span className="text-primary">Rider</span></h2>
            <p className="text-muted" style={{fontSize: '0.875rem'}}>Ingresa tus credenciales para continuar</p>
          </div>
          <InputField label="Email" icon={Mail} type="email" placeholder="tu@email.com" />
          <InputField label="Contraseña" icon={Lock} type="password" placeholder="••••••••" />
          <button onClick={() => navigate('/dashboard')} className="btn btn-primary mt-6" style={{width: '100%'}}>Entrar al Garage</button>
          <p className="text-center mt-6 text-muted" style={{fontSize: '0.875rem'}}>
            ¿No tienes cuenta? <span className="text-primary" style={{cursor: 'pointer'}}>Regístrate aquí</span>
          </p>
        </GlassCard>
      </motion.div>
    </div>
  );
};

const DashboardView = () => {
  // Panamá center coords
  const position = [8.9824, -79.5199]; 
  
  return (
    <div className="container py-12">
      <div className="grid grid-cols-1 md-grid-cols-4 gap-6 mb-12">
        <GlassCard className="text-center">
          <Trophy className="mx-auto mb-2 text-primary" size={32} />
          <p className="input-label">Puntos Totales</p>
          <h3 className="text-3xl">4,250</h3>
        </GlassCard>
        <GlassCard className="text-center">
          <MapPin className="mx-auto mb-2" style={{color: 'var(--info)'}} size={32} />
          <p className="input-label">Stickers Escaneados</p>
          <h3 className="text-3xl">12/45</h3>
        </GlassCard>
        <GlassCard className="text-center">
          <Zap className="mx-auto mb-2" style={{color: '#F97316'}} size={32} />
          <p className="input-label">Rango Global</p>
          <h3 className="text-3xl">#14</h3>
        </GlassCard>
        <GlassCard className="text-center">
          <ShieldCheck className="mx-auto mb-2" style={{color: 'var(--success)'}} size={32} />
          <p className="input-label">Provincias</p>
          <h3 className="text-3xl">3/9</h3>
        </GlassCard>
      </div>

      <div className="grid grid-cols-1 md-grid-cols-3 gap-8">
        <div className="md-col-span-2">
          <h2 className="text-2xl mb-6 flex items-center gap-2"><MapPin className="text-primary" /> Mapa de la Temporada</h2>
          <div className="glass-card" style={{padding: '0', overflow: 'hidden'}}>
            <MapContainer center={position} zoom={13} scrollWheelZoom={false}>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Marker position={position}>
                <Popup>
                  Punto de Escaneo Oficial. <br /> Taller Moto507.
                </Popup>
              </Marker>
            </MapContainer>
          </div>
        </div>
        <div>
          <h2 className="text-2xl mb-6 flex items-center gap-2"><QrCode className="text-primary" /> Escaneo Rápido</h2>
          <GlassCard>
            <div className="flex items-center justify-center mb-6" style={{aspectRatio: '1', background: 'rgba(255,255,255,0.05)', borderRadius: '1rem', border: '2px dashed var(--border)'}}>
              <QrCode size={64} style={{color: 'rgba(255,255,255,0.2)'}} />
            </div>
            <button className="btn btn-primary" style={{width: '100%'}}>Abrir Cámara</button>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};

const AdminView = () => (
  <div className="container py-12">
    <div className="flex items-center justify-between mb-12">
      <h2 className="text-3xl">Admin <span className="text-primary">Control</span></h2>
      <button className="btn btn-primary"><PlusCircle size={20}/> Nuevo Sticker QR</button>
    </div>
    <div className="grid grid-cols-1 md-grid-cols-3 gap-8">
      <GlassCard className="md-col-span-2">
        <h3 className="text-xl mb-6 flex items-center gap-2"><BarChart3 size={20}/> Actividad en Tiempo Real</h3>
        <div className="flex-col gap-4">
          {[1,2,3].map(i => (
            <div key={i} className="flex items-center justify-between mb-4" style={{padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '12px'}}>
              <div className="flex items-center gap-4">
                <div className="flex items-center justify-center text-primary" style={{width: '40px', height: '40px', background: 'rgba(255, 215, 0, 0.2)', borderRadius: '50%', fontSize: '0.75rem', fontWeight: 'bold'}}>R{i}</div>
                <div>
                  <p style={{fontSize: '0.875rem', fontWeight: 'bold'}}>Rider_{i+100} escaneó "Mirador Campana"</p>
                  <p className="text-muted" style={{fontSize: '0.625rem'}}>Hace 2 minutos • GPS Validado ✅</p>
                </div>
              </div>
              <div className="text-primary" style={{fontWeight: 'bold'}}>+50 pts</div>
            </div>
          ))}
        </div>
      </GlassCard>
      <GlassCard>
        <h3 className="text-xl mb-6">Estado Temporada</h3>
        <div style={{padding: '1rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.2)', borderRadius: '12px', marginBottom: '1rem'}}>
          <p className="input-label" style={{color: 'var(--success)'}}>Activa</p>
          <p className="text-xl">Temporada Génesis</p>
        </div>
        <p className="text-muted" style={{fontSize: '0.875rem'}}>Días restantes: 142</p>
        <hr className="mb-6 mt-6" style={{borderColor: 'var(--border)'}} />
        <button className="btn btn-outline" style={{width: '100%'}}>Gestionar Premios</button>
      </GlassCard>
    </div>
  </div>
);

// --- APP PRINCIPAL ---

export default function App() {
  const location = useLocation();

  return (
    <div className="min-h-screen">
      <div className="asphalt-texture"></div>
      
      {/* Navbar Website */}
      <nav className="navbar py-6">
        <div className="container flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2" style={{textDecoration: 'none', color: 'var(--text)'}}>
            <div className="flex items-center justify-center text-black" style={{width: '32px', height: '32px', background: 'var(--primary)', borderRadius: '8px', fontWeight: '900'}}>C</div>
            <span style={{fontWeight: '900', letterSpacing: '-0.05em', fontSize: '1.25rem'}}>CILINDRAJE 507</span>
          </Link>
          <div className="nav-links">
            <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>Inicio</Link>
            <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Dashboard</Link>
            <Link to="/admin" className={`nav-link ${location.pathname === '/admin' ? 'active' : ''}`}>Admin</Link>
            <Link to="/login" className="btn btn-primary" style={{padding: '0.5rem 1.5rem', fontSize: '0.875rem'}}>Login</Link>
          </div>
        </div>
      </nav>

      <main style={{minHeight: '80vh'}}>
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }}><LandingView /></motion.div>} />
            <Route path="/login" element={<motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}><LoginView /></motion.div>} />
            <Route path="/dashboard" element={<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}><DashboardView /></motion.div>} />
            <Route path="/admin" element={<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}><AdminView /></motion.div>} />
          </Routes>
        </AnimatePresence>
      </main>

      <footer className="site-footer">
        Cilindraje 507 &copy; 2026 | Built by Jarvisin OS
      </footer>
    </div>
  );
}
