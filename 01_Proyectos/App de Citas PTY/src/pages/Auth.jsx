import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulación de auth
    navigate('/feed');
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem', textAlign: 'center' }}>
          {isLogin ? 'Bienvenido' : 'Únete al Patio'}
        </h2>
        <p style={{ color: 'var(--text-muted)', textAlign: 'center', marginBottom: '2rem' }}>
          {isLogin ? 'Ingresa tus credenciales premium' : 'Empieza a vivir planes reales en PTY'}
        </p>

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="input-group">
              <label>Nombre Completo</label>
              <input type="text" placeholder="Ej. Juan Pérez" required />
            </div>
          )}
          <div className="input-group">
            <label>Correo Electrónico</label>
            <input type="email" placeholder="tu@email.com" required />
          </div>
          <div className="input-group">
            <label>Contraseña</label>
            <input type="password" placeholder="••••••••" required />
          </div>

          <button type="submit" className="btn-primary">
            {isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}
          </button>
        </form>

        <p style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          {isLogin ? '¿No tienes cuenta?' : '¿Ya eres miembro?'} {' '}
          <span 
            onClick={() => setIsLogin(!isLogin)} 
            style={{ color: 'var(--primary)', cursor: 'pointer', fontWeight: 600 }}
          >
            {isLogin ? 'Regístrate aquí' : 'Inicia sesión'}
          </span>
        </p>
      </div>
    </div>
  );
};

export default Auth;
