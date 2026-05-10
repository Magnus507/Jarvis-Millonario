import React from 'react';
import { Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  Trophy, MapPin, QrCode, Zap, ChevronRight, 
  ShieldCheck, Lock, Mail, BarChart3, PlusCircle, Skull, Flag
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import { factions, stickers, currentUser, territories } from './mockDb';

// --- COMPONENTES DE UI REUTILIZABLES ---
const GlassCard = ({ children, className = "", style = {} }) => (
  <div className={`glass-card ${className}`} style={style}>
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
        <span className="neon-text mb-4" style={{display: 'block', fontWeight: 'bold', tracking: '0.1em', fontSize: '0.875rem'}}>LA GUERRA POR LAS PROVINCIAS HA COMENZADO</span>
        <h1 className="text-6xl mb-6">Cilindraje <span className="neon-text">507</span></h1>
        <p className="text-xl text-muted mx-auto mb-12" style={{maxWidth: '42rem'}}>
          Únete a una facción. Escanea Nodos QR. Domina el territorio.
          El juego nacional donde tu moto es tu arma táctica.
        </p>
        <div className="flex justify-center gap-4">
          <button onClick={() => navigate('/login')} className="btn btn-primary">
            Alistarse <ChevronRight size={20} />
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
            <Skull className="mx-auto mb-4 text-primary" size={40} />
            <h2 className="text-3xl mb-2">Conectar <span className="text-primary">HUD</span></h2>
            <p className="text-muted" style={{fontSize: '0.875rem'}}>Accede a la red táctica</p>
          </div>
          <InputField label="Identificación (Email)" icon={Mail} type="email" placeholder="rider@faccion.com" />
          <InputField label="Código de Acceso" icon={Lock} type="password" placeholder="••••••••" />
          
          <div className="mt-4 mb-2">
            <label className="input-label">Seleccionar Facción (Nuevos)</label>
            <div className="grid grid-cols-2 gap-2 mt-2">
              {factions.map(f => (
                <div key={f.id} className="p-2 border rounded" style={{borderColor: f.color, color: f.color, fontSize: '0.75rem', textAlign: 'center', cursor: 'pointer', background: 'rgba(255,255,255,0.02)'}}>
                  {f.name}
                </div>
              ))}
            </div>
          </div>

          <button onClick={() => navigate('/dashboard')} className="btn btn-primary mt-6" style={{width: '100%'}}>Sincronizar</button>
        </GlassCard>
      </motion.div>
    </div>
  );
};

const DashboardView = () => {
  const position = [8.9824, -79.5199]; 
  const userFaction = factions.find(f => f.id === currentUser.faction_id);
  
  // Helpers para colores de rareza
  const getRarityColor = (rarity) => {
    switch(rarity) {
      case 'legendary': return '#F59E0B'; // Ambar/Oro
      case 'epic': return '#8B5CF6'; // Violeta
      case 'rare': return '#3B82F6'; // Azul
      default: return '#10B981'; // Verde (normal)
    }
  };

  return (
    <div className="container py-12">
      {/* HUD HEADER */}
      <div className="flex items-center justify-between mb-8" style={{borderBottom: `2px solid ${userFaction.color}40`, paddingBottom: '1rem'}}>
        <div>
          <h2 className="text-3xl" style={{color: userFaction.color}}>{currentUser.username}</h2>
          <p className="text-muted text-sm uppercase tracking-widest flex items-center gap-2">
            <Flag size={14} color={userFaction.color} /> {userFaction.name} Operative
          </p>
        </div>
        <div className="text-right">
          <p className="text-3xl neon-text">{currentUser.total_points}</p>
          <p className="input-label">Puntos de Contribución</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md-grid-cols-4 gap-6 mb-12">
        {territories.map(t => {
          const owner = factions.find(f => f.id === t.controlling_faction_id);
          return (
            <GlassCard key={t.id} className="text-center" style={{borderTop: `4px solid ${owner.color}`}}>
              <MapPin className="mx-auto mb-2" style={{color: owner.color}} size={24} />
              <p className="text-sm font-bold uppercase">{t.name}</p>
              <p style={{fontSize: '0.65rem', color: 'var(--text-muted)'}}>{owner.name}</p>
            </GlassCard>
          )
        })}
      </div>

      <div className="grid grid-cols-1 md-grid-cols-3 gap-8">
        <div className="md-col-span-2">
          <h2 className="text-2xl mb-6 flex items-center gap-2"><MapPin className="text-primary" /> Radar Cyberpunk</h2>
          <div className="glass-card" style={{padding: '0', overflow: 'hidden', border: '1px solid rgba(255,215,0,0.3)', boxShadow: '0 0 20px rgba(255,215,0,0.05)'}}>
            <MapContainer center={position} zoom={12} scrollWheelZoom={false}>
              {/* CartoDB Dark Matter para estética Cyberpunk/Radar */}
              <TileLayer
                attribution='&copy; <a href="https://carto.com/">CartoDB</a>'
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              />
              {stickers.map(s => (
                <CircleMarker 
                  key={s.id} 
                  center={[s.lat, s.lng]} 
                  pathOptions={{ color: getRarityColor(s.rarity), fillColor: getRarityColor(s.rarity), fillOpacity: 0.5 }}
                  radius={8}
                >
                  <Popup>
                    <div style={{background: 'var(--surface)', color: 'var(--text)', padding: '5px'}}>
                      <strong style={{color: getRarityColor(s.rarity), textTransform: 'uppercase'}}>{s.name}</strong><br />
                      Rareza: {s.rarity} (+{s.points} pts)<br />
                      Tipo: {s.type}
                    </div>
                  </Popup>
                </CircleMarker>
              ))}
            </MapContainer>
          </div>
        </div>
        <div>
          <h2 className="text-2xl mb-6 flex items-center gap-2"><QrCode className="text-primary" /> Enlace Táctico</h2>
          <GlassCard>
            <div className="flex items-center justify-center mb-6" style={{aspectRatio: '1', background: 'rgba(255,255,255,0.02)', borderRadius: '1rem', border: '2px dashed rgba(255,215,0,0.3)', position: 'relative', overflow: 'hidden'}}>
               {/* Simulación de scan line */}
               <div style={{position: 'absolute', top: '0', left: '0', right: '0', height: '2px', background: 'var(--primary)', boxShadow: '0 0 10px var(--primary)', animation: 'scan 2s infinite linear'}}></div>
              <QrCode size={64} style={{color: 'rgba(255,215,0,0.2)'}} />
            </div>
            <button className="btn btn-primary" style={{width: '100%'}}>Iniciar Escaneo (Activar Cámara)</button>
            <p className="text-center mt-4 text-muted" style={{fontSize: '0.65rem'}}>Verificando Anti-Spoofing GPS...</p>
          </GlassCard>
        </div>
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes scan {
          0% { top: 0; }
          50% { top: 100%; }
          100% { top: 0; }
        }
      `}} />
    </div>
  );
};

const AdminView = () => (
  <div className="container py-12">
    <div className="flex items-center justify-between mb-12">
      <h2 className="text-3xl">Overwatch <span className="text-primary">Control</span></h2>
      <button className="btn btn-primary"><PlusCircle size={20}/> Desplegar Nodo QR</button>
    </div>
    <div className="grid grid-cols-1 md-grid-cols-3 gap-8">
      <GlassCard className="md-col-span-2">
        <h3 className="text-xl mb-6 flex items-center gap-2"><BarChart3 size={20}/> Monitor Anti-Cheat & Actividad</h3>
        <div className="flex-col gap-4">
          {[
            { rider: 'Rider_Alpha', action: 'Escaneó Taller Moto507', status: 'GPS Validado ✅', points: '+1000' },
            { rider: 'Ghost_99', action: 'Escaneó Mirador Campana', status: 'GPS Spoofing Detectado ❌', points: 'FLAGGED' },
          ].map((log, i) => (
            <div key={i} className="flex items-center justify-between mb-4" style={{padding: '1rem', background: 'rgba(255,255,255,0.02)', borderLeft: log.points === 'FLAGGED' ? '3px solid red' : '3px solid green', borderRadius: '4px'}}>
              <div className="flex items-center gap-4">
                <div>
                  <p style={{fontSize: '0.875rem', fontWeight: 'bold'}}>{log.rider} <span className="text-muted font-normal">{log.action}</span></p>
                  <p className="text-muted" style={{fontSize: '0.625rem', color: log.points === 'FLAGGED' ? '#EF4444' : '#10B981'}}>{log.status}</p>
                </div>
              </div>
              <div style={{fontWeight: 'bold', color: log.points === 'FLAGGED' ? '#EF4444' : 'var(--primary)'}}>{log.points}</div>
            </div>
          ))}
        </div>
      </GlassCard>
      <GlassCard>
        <h3 className="text-xl mb-6">Guerra de Facciones</h3>
        <div className="flex-col gap-2">
          {factions.map(f => {
            const owned = territories.filter(t => t.controlling_faction_id === f.id).length;
            return (
              <div key={f.id} className="flex justify-between items-center p-2 mb-2 rounded" style={{background: 'rgba(255,255,255,0.02)', borderRight: `4px solid ${f.color}`}}>
                <span style={{fontSize: '0.75rem', color: f.color}}>{f.name}</span>
                <span className="text-sm font-bold">{owned} Provincias</span>
              </div>
            )
          })}
        </div>
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
      
      <nav className="navbar py-6">
        <div className="container flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2" style={{textDecoration: 'none', color: 'var(--text)'}}>
            <div className="flex items-center justify-center text-black" style={{width: '32px', height: '32px', background: 'var(--primary)', borderRadius: '8px', fontWeight: '900'}}>C</div>
            <span style={{fontWeight: '900', letterSpacing: '-0.05em', fontSize: '1.25rem'}}>CILINDRAJE 507</span>
          </Link>
          <div className="nav-links">
            <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>Inicio</Link>
            <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>Radar</Link>
            <Link to="/admin" className={`nav-link ${location.pathname === '/admin' ? 'active' : ''}`}>Overwatch</Link>
            <Link to="/login" className="btn btn-primary" style={{padding: '0.5rem 1.5rem', fontSize: '0.875rem'}}>Desconectar</Link>
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
        Cilindraje 507 &copy; 2026 | Arquitectura Local Preparada para Vercel/Supabase
      </footer>
    </div>
  );
}
