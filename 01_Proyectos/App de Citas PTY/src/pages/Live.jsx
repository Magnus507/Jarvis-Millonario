import React from 'react';
import { Radio, Users, Zap } from 'lucide-react';

const Live = () => {
  const liveStreams = [
    { id: 1, user: "Sofia", viewers: 12, title: "Parking en Costa del Este 🥂", tags: ["Nightlife", "Vip"] },
    { id: 2, user: "Andres", viewers: 45, title: "Probando el nuevo spot de Burger 🍔", tags: ["Foodie", "RealTime"] },
    { id: 3, user: "Valeria", viewers: 8, title: "Sunset en el Causeway 🌅", tags: ["Relax", "Outdoors"] },
  ];

  return (
    <div className="live-container">
      <header style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
          <div className="live-indicator"></div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 800 }}>En Vivo</h1>
        </div>
        <p style={{ color: 'var(--text-muted)' }}>Mira lo que está pasando en PTY ahora mismo.</p>
      </header>

      <div className="live-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '2rem' }}>
        {liveStreams.map(stream => (
          <div key={stream.id} className="live-card">
            <div className="live-preview">
              <div className="live-tag">
                <Radio size={14} /> EN VIVO
              </div>
              <div className="viewer-count">
                <Users size={14} /> {stream.viewers}
              </div>
            </div>
            <div className="live-info">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', marginBottom: '0.5rem' }}>
                <div className="user-avatar-small"></div>
                <span style={{ fontWeight: 600 }}>@{stream.user}</span>
              </div>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>{stream.title}</h3>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                {stream.tags.map(tag => (
                  <span key={tag} className="tag-pill">{tag}</span>
                ))}
              </div>
              <button className="btn-secondary" style={{ marginTop: '1.5rem', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                <Zap size={18} /> Unirse al plan
              </button>
            </div>
          </div>
        ))}
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .live-indicator {
          width: 12px;
          height: 12px;
          background: #ff4d4d;
          border-radius: 50%;
          box-shadow: 0 0 15px #ff4d4d;
          animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
          0% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.3); opacity: 0.5; }
          100% { transform: scale(1); opacity: 1; }
        }

        .live-card {
          background: var(--bg-card);
          border: 1px solid var(--glass-border);
          border-radius: 28px;
          overflow: hidden;
          transition: transform 0.3s ease;
        }

        .live-card:hover {
          transform: translateY(-5px);
          border-color: var(--secondary);
        }

        .live-preview {
          height: 200px;
          background: linear-gradient(45deg, #1a1c23, #0f1118);
          position: relative;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .live-tag {
          position: absolute;
          top: 1rem;
          left: 1rem;
          background: #ff4d4d;
          color: white;
          padding: 0.3rem 0.8rem;
          border-radius: 8px;
          font-size: 0.7rem;
          font-weight: 800;
          display: flex;
          align-items: center;
          gap: 0.4rem;
        }

        .viewer-count {
          position: absolute;
          top: 1rem;
          right: 1rem;
          background: rgba(0,0,0,0.6);
          backdrop-filter: blur(10px);
          color: white;
          padding: 0.3rem 0.8rem;
          border-radius: 8px;
          font-size: 0.7rem;
          display: flex;
          align-items: center;
          gap: 0.4rem;
        }

        .live-info {
          padding: 1.5rem;
        }

        .user-avatar-small {
          width: 32px;
          height: 32px;
          background: var(--primary);
          border-radius: 50%;
        }

        .tag-pill {
          font-size: 0.7rem;
          background: var(--glass);
          border: 1px solid var(--glass-border);
          padding: 0.2rem 0.6rem;
          border-radius: 20px;
          color: var(--text-muted);
        }

        .btn-secondary {
          background: rgba(110, 69, 226, 0.2);
          border: 1px solid var(--secondary);
          color: var(--secondary);
          padding: 0.8rem;
          border-radius: 12px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-secondary:hover {
          background: var(--secondary);
          color: white;
        }
      `}} />
    </div>
  );
};

export default Live;
