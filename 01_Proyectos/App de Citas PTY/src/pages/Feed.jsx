import React from 'react';
import { MapPin, Calendar, Users, Star } from 'lucide-react';

const Feed = () => {
  const plans = [
    { 
      id: 1, 
      user: "Elena", 
      plan: "Sushi & Drinks en Casco", 
      time: "Hoy, 8:00 PM", 
      location: "Casco Viejo", 
      category: "GASTRONOMÍA",
      image: "/panama_nightlife_plan_1_1778375856673.png"
    },
    { 
      id: 2, 
      user: "Carlos", 
      plan: "Parking de F1", 
      time: "Mañana, 1:00 PM", 
      location: "Bella Vista", 
      category: "NIGHTLIFE",
      image: "/panama_nightlife_plan_2_1778375898996.png"
    },
    { 
      id: 3, 
      user: "Mari", 
      plan: "Sunset Yoga + Brunch", 
      time: "Domingo, 4:30 PM", 
      location: "Amador", 
      category: "OUTDOOR",
      image: "/panama_sunset_yoga_1778375922358.png"
    }
  ];

  return (
    <div className="feed-container">
      <header style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div>
          <h1 style={{ fontSize: '3rem', fontWeight: 800, marginBottom: '0.5rem' }}>Descubre Planes</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>Gente real, conexiones reales en Panamá.</p>
        </div>
        <button className="btn-primary" style={{ width: 'auto', padding: '0.8rem 2rem' }}>
          + Crear Plan
        </button>
      </header>

      <div className="features-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '2rem' }}>
        {plans.map(p => (
          <div key={p.id} className="plan-card">
            <div className="plan-image-container">
              <img src={p.image} alt={p.plan} className="plan-image" />
              <div className="plan-badge">{p.category}</div>
            </div>
            
            <div className="plan-content">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                  <MapPin size={14} className="icon-gold" /> {p.location}
                </div>
                <div className="rating-tag">
                  <Star size={12} fill="var(--primary)" color="var(--primary)" /> 4.9
                </div>
              </div>

              <h3 style={{ fontSize: '1.4rem', marginBottom: '1rem', fontWeight: 700 }}>{p.plan}</h3>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                <div className="info-pill">
                  <Calendar size={14} /> {p.time}
                </div>
                <div className="info-pill">
                  <Users size={14} /> {p.user}
                </div>
              </div>

              <button className="btn-primary-outline">Me interesa</button>
            </div>
          </div>
        ))}
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .plan-image-container {
          position: relative;
          width: 100%;
          height: 220px;
          border-radius: 20px;
          overflow: hidden;
          margin-bottom: 1.5rem;
        }

        .plan-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.5s ease;
        }

        .plan-card:hover .plan-image {
          transform: scale(1.1);
        }

        .plan-badge {
          position: absolute;
          top: 1rem;
          left: 1rem;
          background: rgba(0,0,0,0.6);
          backdrop-filter: blur(8px);
          padding: 0.4rem 0.8rem;
          border-radius: 10px;
          font-size: 0.7rem;
          font-weight: 700;
          letter-spacing: 1px;
          border: 1px solid rgba(255,255,255,0.1);
        }

        .rating-tag {
          display: flex;
          align-items: center;
          gap: 0.3rem;
          background: rgba(212, 175, 55, 0.1);
          color: var(--primary);
          padding: 0.2rem 0.6rem;
          border-radius: 8px;
          font-size: 0.8rem;
          font-weight: 700;
        }

        .info-pill {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          color: var(--text-muted);
          background: var(--glass);
          padding: 0.4rem 0.8rem;
          border-radius: 10px;
        }

        .icon-gold { color: var(--primary); }

        .btn-primary-outline {
          width: 100%;
          background: transparent;
          border: 1px solid var(--primary);
          color: var(--primary);
          padding: 0.8rem;
          border-radius: 12px;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-primary-outline:hover {
          background: var(--primary);
          color: black;
          box-shadow: 0 0 20px var(--primary-glow);
        }
      `}} />
    </div>
  );
};

export default Feed;

