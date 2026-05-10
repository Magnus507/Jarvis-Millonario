import React from 'react';
import { Heart, MessageCircle, UserX } from 'lucide-react';

const Matches = () => {
  const matches = [
    { id: 1, name: "Sofia", status: "En línea", lastMsg: "¡Nos vemos en Casco!" },
    { id: 2, name: "Valeria", status: "Hace 2h", lastMsg: "¿A qué hora es el yoga?" },
    { id: 3, name: "Isabella", status: "En línea", lastMsg: "Me encanta el plan de F1" },
  ];

  return (
    <div className="matches-container">
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800 }}>Tus Matches</h1>
        <p style={{ color: 'var(--text-muted)' }}>Conexiones listas para concretar planes.</p>
      </header>

      <div className="matches-list">
        {matches.map(m => (
          <div key={m.id} className="match-row">
            <div className="match-avatar"></div>
            <div className="match-info">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h3>{m.name}</h3>
                <span className={`status-dot ${m.status === 'En línea' ? 'online' : ''}`}></span>
              </div>
              <p>{m.lastMsg}</p>
            </div>
            <div className="match-actions">
              <button className="action-btn chat"><MessageCircle size={18} /></button>
              <button className="action-btn unmatch"><UserX size={18} /></button>
            </div>
          </div>
        ))}
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .match-row {
          background: var(--bg-card);
          border: 1px solid var(--glass-border);
          padding: 1.2rem;
          border-radius: 20px;
          display: flex;
          align-items: center;
          gap: 1.5rem;
          margin-bottom: 1rem;
          transition: all 0.2s;
        }

        .match-row:hover {
          transform: scale(1.01);
          border-color: var(--primary);
        }

        .match-avatar {
          width: 60px;
          height: 60px;
          background: var(--glass);
          border-radius: 18px;
        }

        .match-info { flex: 1; }
        .match-info h3 { font-size: 1.1rem; margin-bottom: 0.2rem; }
        .match-info p { font-size: 0.9rem; color: var(--text-muted); }

        .status-dot {
          width: 8px;
          height: 8px;
          background: var(--text-muted);
          border-radius: 50%;
        }

        .status-dot.online {
          background: #00ff88;
          box-shadow: 0 0 10px #00ff88;
        }

        .match-actions { display: flex; gap: 0.8rem; }
        
        .action-btn {
          width: 40px;
          height: 40px;
          border-radius: 12px;
          border: 1px solid var(--glass-border);
          background: transparent;
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.2s;
        }

        .action-btn.chat:hover { background: var(--primary); color: black; }
        .action-btn.unmatch:hover { background: var(--accent); color: white; }
      `}} />
    </div>
  );
};

export default Matches;
