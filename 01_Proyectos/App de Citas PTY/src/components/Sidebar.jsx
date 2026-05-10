import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutGrid, Radio, Heart, User, Settings, LogOut } from 'lucide-react';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="logo-area" style={{ marginBottom: '3rem', padding: '0 1rem' }}>
        <h2 className="gradient-text" style={{ fontSize: '1.5rem', fontWeight: 800 }}>PATIO PTY</h2>
      </div>
      
      <nav style={{ flex: 1 }}>
        <NavLink to="/feed" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <LayoutGrid /> <span>Planes</span>
        </NavLink>
        <NavLink to="/live" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Radio /> <span>En Vivo</span>
        </NavLink>
        <NavLink to="/matches" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Heart /> <span>Matches</span>
        </NavLink>
        <NavLink to="/profile" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <User /> <span>Perfil</span>
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <NavLink to="/settings" className="nav-link">
          <Settings /> <span>Ajustes</span>
        </NavLink>
        <button onClick={() => window.location.href = '/'} className="nav-link" style={{ width: '100%', background: 'none', border: 'none', textAlign: 'left', cursor: 'pointer' }}>
          <LogOut /> <span>Salir</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
