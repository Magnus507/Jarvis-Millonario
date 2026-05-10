import React from 'react';
import { User, Shield, Bell, CreditCard, ChevronRight } from 'lucide-react';

const Profile = () => {
  return (
    <div className="profile-container" style={{ maxWidth: '800px' }}>
      <header style={{ marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800 }}>Mi Perfil</h1>
        <p style={{ color: 'var(--text-muted)' }}>Gestiona tu privacidad y presencia en el Patio.</p>
      </header>

      <div className="profile-header-card">
        <div className="profile-avatar-large">
          <div className="avatar-edit">Editar</div>
        </div>
        <div className="profile-main-info">
          <h2 style={{ fontSize: '1.8rem' }}>Geankarlos M.</h2>
          <p style={{ color: 'var(--primary)', fontWeight: 600 }}>Miembro Fundador • Panamá, PTY</p>
          <div className="profile-stats">
            <div className="stat-item">
              <strong>12</strong>
              <span>Planes</span>
            </div>
            <div className="stat-item">
              <strong>156</strong>
              <span>Conexiones</span>
            </div>
            <div className="stat-item">
              <strong>4.9</strong>
              <span>Rating</span>
            </div>
          </div>
        </div>
      </div>

      <div className="settings-grid">
        <div className="settings-section">
          <h3>Privacidad Progresiva</h3>
          <div className="settings-item">
            <div className="item-icon"><Shield size={20} /></div>
            <div className="item-content">
              <h4>Visibilidad de Perfil</h4>
              <p>Solo visible para matches confirmados.</p>
            </div>
            <ChevronRight className="chevron" />
          </div>
          <div className="settings-item">
            <div className="item-icon"><User size={20} /></div>
            <div className="item-content">
              <h4>Verificación de Identidad</h4>
              <p>Estado: <span style={{ color: '#00ff88' }}>Verificado</span></p>
            </div>
            <ChevronRight className="chevron" />
          </div>
        </div>

        <div className="settings-section">
          <h3>Cuenta y Notificaciones</h3>
          <div className="settings-item">
            <div className="item-icon"><Bell size={20} /></div>
            <div className="item-content">
              <h4>Notificaciones Push</h4>
              <p>Alertas de planes cerca de ti.</p>
            </div>
            <ChevronRight className="chevron" />
          </div>
          <div className="settings-item">
            <div className="item-icon"><CreditCard size={20} /></div>
            <div className="item-content">
              <h4>Suscripción Premium</h4>
              <p>Patio Gold • Renueva en 15 días.</p>
            </div>
            <ChevronRight className="chevron" />
          </div>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .profile-header-card {
          background: var(--bg-card);
          border: 1px solid var(--glass-border);
          padding: 2.5rem;
          border-radius: 32px;
          display: flex;
          gap: 2.5rem;
          align-items: center;
          margin-bottom: 3rem;
        }

        @media (max-width: 600px) {
          .profile-header-card { flex-direction: column; text-align: center; }
        }

        .profile-avatar-large {
          width: 140px;
          height: 140px;
          background: linear-gradient(135deg, #1a1c23, #0f1118);
          border: 2px solid var(--primary);
          border-radius: 40px;
          position: relative;
        }

        .avatar-edit {
          position: absolute;
          bottom: -10px;
          left: 50%;
          transform: translateX(-50%);
          background: var(--primary);
          color: black;
          padding: 0.3rem 0.8rem;
          border-radius: 8px;
          font-size: 0.7rem;
          font-weight: 700;
          cursor: pointer;
        }

        .profile-stats {
          display: flex;
          gap: 2rem;
          margin-top: 1.5rem;
        }

        .stat-item {
          display: flex;
          flex-direction: column;
        }

        .stat-item strong { font-size: 1.2rem; }
        .stat-item span { font-size: 0.8rem; color: var(--text-muted); }

        .settings-section {
          margin-bottom: 2.5rem;
        }

        .settings-section h3 {
          font-size: 0.9rem;
          color: var(--text-muted);
          text-transform: uppercase;
          letter-spacing: 1.5px;
          margin-bottom: 1rem;
          padding-left: 0.5rem;
        }

        .settings-item {
          background: var(--bg-card);
          border: 1px solid var(--glass-border);
          padding: 1.2rem;
          border-radius: 16px;
          display: flex;
          align-items: center;
          gap: 1.2rem;
          margin-bottom: 0.8rem;
          cursor: pointer;
          transition: all 0.2s;
        }

        .settings-item:hover {
          border-color: var(--glass-border);
          background: rgba(255,255,255,0.02);
          transform: translateX(5px);
        }

        .item-icon {
          width: 40px;
          height: 40px;
          background: var(--glass);
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--primary);
        }

        .item-content h4 { font-size: 1rem; margin-bottom: 0.2rem; }
        .item-content p { font-size: 0.85rem; color: var(--text-muted); }

        .chevron {
          margin-left: auto;
          color: var(--text-muted);
          opacity: 0.5;
        }
      `}} />
    </div>
  );
};

export default Profile;
