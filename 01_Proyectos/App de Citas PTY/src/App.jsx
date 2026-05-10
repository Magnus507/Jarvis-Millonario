import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Auth from './pages/Auth';
import Feed from './pages/Feed';
import Live from './pages/Live';
import Profile from './pages/Profile';
import Matches from './pages/Matches';
import './index.css';

// Componente para manejar el Layout condicional
const AppLayout = ({ children }) => {
  const location = useLocation();
  const isAuthPage = location.pathname === '/' || location.pathname === '/auth';

  return (
    <div className="app-shell">
      {!isAuthPage && <Sidebar />}
      <main className={isAuthPage ? 'auth-main' : 'main-content'}>
        {children}
      </main>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Auth />} />
          <Route path="/feed" element={<Feed />} />
          <Route path="/live" element={<Live />} />
          <Route path="/matches" element={<Matches />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Profile />} /> {/* Usamos Profile como base por ahora */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;

