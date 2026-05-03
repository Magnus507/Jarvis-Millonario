/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Heart, 
  MessageCircle, 
  MapPin, 
  Video, 
  User, 
  Zap, 
  Search, 
  Filter,
  Check,
  X,
  Navigation,
  Clock,
  ShieldCheck
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// --- Types ---

type IntentionColor = 'green' | 'yellow' | 'red';

interface Profile {
  id: string;
  username: string;
  age: number;
  bio: string;
  intention_color: IntentionColor;
  avatar_url: string;
  last_seen: string;
}

interface Plan {
  id: string;
  name: string;
  description: string;
  location: string;
  time: string;
  color: IntentionColor;
}

// --- Components ---

const SemaphoreBadge = ({ color }: { color: IntentionColor }) => {
  const colors = {
    green: 'bg-[#00FF66] shadow-[0_0_10px_#00FF66]',
    yellow: 'bg-[#FFDE00] shadow-[0_0_10px_#FFDE00]',
    red: 'bg-[#FF0000] shadow-[0_0_10px_#FF0000]',
  };
  
  return (
    <div className={`w-3 h-3 rounded-full ${colors[color]}`} />
  );
};

const LuxeCard = ({ children, className = '' }: { children: React.ReactNode, className?: string }) => (
  <div className={`bg-neutral-900/80 backdrop-blur-md border border-[#D4AF37]/20 rounded-2xl overflow-hidden ${className}`}>
    {children}
  </div>
);

// --- Main App ---

export default function App() {
  const [activeTab, setActiveTab] = useState<'plans' | 'explore' | 'xopa' | 'messages' | 'profile'>('explore');
  const [userIntention, setUserIntention] = useState<IntentionColor>('green');
  const [isXopaActive, setIsXopaActive] = useState(false);
  const [xopaTimer, setXopaTimer] = useState(180); // 3 minutes
  const [blurLevel, setBlurLevel] = useState(20);
  
  // Fake data for UI prototype
  const mockPlans: Plan[] = [
    { id: '1', name: 'Almuerzo en Casco', description: 'Buscando gente para ir a Maito.', location: 'Casco Viejo', time: '2:00 PM', color: 'green' },
    { id: '2', name: 'Drinks en la Terraza', description: 'Plan tranqui después de trabajar.', location: 'Punta Pacifica', time: '7:30 PM', color: 'yellow' },
    { id: '3', name: 'Salida de Discoteca', description: 'Directo al afterparty.', location: 'Calle Uruguay', time: '1:00 AM', color: 'red' },
  ];

  const mockProfiles: Profile[] = [
    { id: '1', username: 'Andre_PTY', age: 24, bio: 'Amo el sushi y los roadtrips.', intention_color: 'green', avatar_url: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&h=400&fit=crop', last_seen: 'Justo ahora' },
    { id: '2', username: 'Maria_Vibes', age: 22, bio: 'Buscando nuevas experiencias.', intention_color: 'yellow', avatar_url: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop', last_seen: 'hace 5 min' },
    { id: '3', username: 'Luis_VIP', age: 28, bio: 'Solo planes exclusivos.', intention_color: 'red', avatar_url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop', last_seen: 'hace 15 min' },
  ];

  // Logic for filtering by intention and activity is simulated here
  const filteredProfiles = mockProfiles.filter(p => p.intention_color === userIntention);

  // Xopa Direct Timer Effect
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isXopaActive && xopaTimer > 0) {
      interval = setInterval(() => {
        setXopaTimer(prev => {
          const next = prev - 1;
          // Progressively clear blur every 30 seconds
          if ((180 - next) % 30 === 0 && next > 0) {
            setBlurLevel(prevBlur => Math.max(0, prevBlur - 4));
          }
          return next;
        });
      }, 1000);
    } else if (xopaTimer === 0) {
      setIsXopaActive(false);
      setXopaTimer(180);
      setBlurLevel(20);
    }
    return () => clearInterval(interval);
  }, [isXopaActive, xopaTimer]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-[#D4AF37]/30">
      {/* --- Header --- */}
      <header className="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-xl border-b border-[#D4AF37]/10 px-6 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tighter text-[#D4AF37]">QXOPA<span className="text-white">?</span></h1>
        
        <div className="flex items-center gap-3 bg-neutral-900 px-3 py-1.5 rounded-full border border-white/5">
          <button 
            onClick={() => setUserIntention('green')}
            className={`w-4 h-4 rounded-full transition-all ${userIntention === 'green' ? 'bg-[#00FF66] scale-125 shadow-[0_0_15px_#00FF66]' : 'bg-[#00FF66]/20'}`}
          />
          <button 
            onClick={() => setUserIntention('yellow')}
            className={`w-4 h-4 rounded-full transition-all ${userIntention === 'yellow' ? 'bg-[#FFDE00] scale-125 shadow-[0_0_15px_#FFDE00]' : 'bg-[#FFDE00]/20'}`}
          />
          <button 
            onClick={() => setUserIntention('red')}
            className={`w-4 h-4 rounded-full transition-all ${userIntention === 'red' ? 'bg-[#FF0000] scale-125 shadow-[0_0_15px_#FF0000]' : 'bg-[#FF0000]/20'}`}
          />
        </div>
      </header>

      {/* --- Main Content --- */}
      <main className="pt-24 pb-32 px-6 max-w-md mx-auto">
        
        <AnimatePresence mode="wait">
          {activeTab === 'explore' && (
            <motion.div 
              key="explore"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold flex items-center gap-2">
                  <Navigation className="w-5 h-5 text-[#D4AF37]" />
                  Gente Cerca
                </h2>
                <span className="text-xs text-neutral-500 uppercase tracking-widest">Panamá City</span>
              </div>

              <div className="grid gap-4">
                {filteredProfiles.length > 0 ? (
                  filteredProfiles.map(profile => (
                    <LuxeCard key={profile.id} className="p-4 flex items-center gap-4 group hover:border-[#D4AF37]/40 transition-colors">
                      <div className="relative">
                        <img src={profile.avatar_url} alt={profile.username} className="w-16 h-16 rounded-full object-cover border-2 border-[#D4AF37]/20" />
                        <div className="absolute -bottom-1 -right-1">
                          <SemaphoreBadge color={profile.intention_color} />
                        </div>
                      </div>
                      <div className="flex-1">
                        <div className="flex justify-between items-start">
                          <h3 className="font-bold text-lg">{profile.username}, {profile.age}</h3>
                          <span className="text-[10px] text-[#00FF66] flex items-center gap-1 font-medium bg-[#00FF66]/10 px-2 py-0.5 rounded-full">
                            <Clock className="w-3 h-3" /> {profile.last_seen}
                          </span>
                        </div>
                        <p className="text-sm text-neutral-400 line-clamp-1">{profile.bio}</p>
                      </div>
                      <button className="p-2 bg-[#D4AF37]/10 rounded-full text-[#D4AF37] hover:bg-[#D4AF37] hover:text-black transition-all">
                        <Heart className="w-5 h-5" />
                      </button>
                    </LuxeCard>
                  ))
                ) : (
                  <div className="text-center py-20 text-neutral-500">
                    <Search className="w-12 h-12 mx-auto mb-4 opacity-20" />
                    <p>No hay perfiles activos con esta intención.</p>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {activeTab === 'plans' && (
            <motion.div 
              key="plans"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold flex items-center gap-2">
                  <Zap className="w-5 h-5 text-[#D4AF37]" />
                  Parkings de Hoy
                </h2>
                <button className="text-[#D4AF37] text-sm">+ Crear Plan</button>
              </div>

              <div className="space-y-4">
                {mockPlans.map(plan => (
                  <LuxeCard key={plan.id} className="p-5 border-l-4 border-l-[#D4AF37]">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="text-lg font-bold">{plan.name}</h3>
                      <SemaphoreBadge color={plan.color} />
                    </div>
                    <p className="text-neutral-400 text-sm mb-4">{plan.description}</p>
                    <div className="flex items-center justify-between text-xs text-neutral-500">
                      <div className="flex items-center gap-3">
                        <span className="flex items-center gap-1"><MapPin className="w-3 h-3" /> {plan.location}</span>
                        <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {plan.time}</span>
                      </div>
                      <button className="text-[#D4AF37] font-semibold border-b border-transparent hover:border-[#D4AF37]">Unirme</button>
                    </div>
                  </LuxeCard>
                ))}
              </div>
            </motion.div>
          )}

          {activeTab === 'xopa' && (
            <motion.div 
              key="xopa"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="h-[60vh] flex flex-col items-center justify-center text-center"
            >
              {!isXopaActive ? (
                <div className="space-y-8">
                  <div className="relative">
                    <div className="absolute inset-0 bg-[#D4AF37]/20 blur-3xl rounded-full scale-150 animate-pulse" />
                    <button 
                      onClick={() => setIsXopaActive(true)}
                      className="relative w-32 h-32 bg-gradient-to-tr from-[#D4AF37] to-[#8A6D3B] rounded-full flex items-center justify-center shadow-[0_0_40px_#D4AF3780] hover:scale-110 active:scale-95 transition-all group"
                    >
                      <Video className="w-12 h-12 text-black transition-transform group-hover:rotate-12" />
                    </button>
                  </div>
                  <div className="space-y-2">
                    <h2 className="text-3xl font-black tracking-tight italic">XOPA DIRECTO</h2>
                    <p className="text-neutral-400 max-w-[250px]">Videochat aleatorio de 3 min con gente a 10km que busca lo mismo que tú.</p>
                  </div>
                  <div className="flex flex-wrap justify-center gap-3">
                    <span className="text-[10px] px-3 py-1 rounded-full border border-white/10 uppercase tracking-widest bg-white/5">Radio: 10km</span>
                    <span className="text-[10px] px-3 py-1 rounded-full border border-white/10 uppercase tracking-widest bg-white/5">Intención: {userIntention}</span>
                  </div>
                </div>
              ) : (
                <div className="w-full h-full relative rounded-3xl overflow-hidden border-2 border-[#D4AF37]">
                  {/* Simulated Video Placeholder */}
                  <div 
                    className="absolute inset-0 bg-neutral-800 bg-cover bg-center"
                    style={{ 
                      backgroundImage: `url(${mockProfiles[1].avatar_url})`,
                      filter: `blur(${blurLevel}px)`,
                      transition: 'filter 2s ease'
                    }}
                  />
                  
                  {/* UI Overlays */}
                  <div className="absolute top-4 left-4 right-4 flex justify-between items-center z-10">
                    <div className="bg-black/50 backdrop-blur-md px-3 py-1 rounded-full flex items-center gap-2 border border-white/10">
                      <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                      <span className="text-xs font-mono">{formatTime(xopaTimer)}</span>
                    </div>
                    <button 
                      onClick={() => { setIsXopaActive(false); setXopaTimer(180); setBlurLevel(20); }}
                      className="p-2 bg-white/10 hover:bg-red-500/80 backdrop-blur-md rounded-xl transition-colors"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>

                  <div className="absolute bottom-6 left-6 flex flex-col gap-1 items-start">
                    <div className="flex items-center gap-2 bg-black/40 backdrop-blur-sm px-3 py-1 rounded-lg">
                      <span className="font-bold">Maria Vibes, 22</span>
                      <SemaphoreBadge color="yellow" />
                    </div>
                    <span className="text-[10px] text-white/60">Buscando un yellow plan...</span>
                  </div>

                  <div className="absolute bottom-6 right-6">
                    <button className="w-12 h-12 bg-[#D4AF37] rounded-full flex items-center justify-center text-black border-4 border-black group">
                      <Heart className="w-6 h-6 group-hover:scale-125 transition-transform" />
                    </button>
                  </div>

                  {/* Progressive Blur Message */}
                  <div className="absolute top-16 left-0 right-0 text-center pointer-events-none">
                    <p className="text-[10px] text-white/40 uppercase tracking-[0.2em] animate-pulse">
                      {blurLevel > 0 ? "Revelando rostro progresivamente..." : "Rostro revelado"}
                    </p>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

      </main>

      {/* --- Tab Bar --- */}
      <nav className="fixed bottom-0 w-full bg-black/90 backdrop-blur-2xl border-t border-[#D4AF37]/10 px-8 py-6 flex justify-between items-center z-50">
        <button 
          onClick={() => setActiveTab('explore')}
          className={`flex flex-col items-center gap-1 transition-colors ${activeTab === 'explore' ? 'text-[#D4AF37]' : 'text-neutral-500'}`}
        >
          <Search className="w-6 h-6" />
        </button>
        <button 
          onClick={() => setActiveTab('plans')}
          className={`flex flex-col items-center gap-1 transition-colors ${activeTab === 'plans' ? 'text-[#D4AF37]' : 'text-neutral-500'}`}
        >
          <Zap className="w-6 h-6" />
        </button>
        
        {/* Center Xopa Toggle */}
        <div className="relative -top-10">
          <button 
            onClick={() => setActiveTab('xopa')}
            className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-all ${activeTab === 'xopa' ? 'bg-[#D4AF37] text-black shadow-[0_10px_30px_#D4AF3740]' : 'bg-neutral-900 text-white border border-[#D4AF37]/20 shadow-2xl'}`}
          >
            <Video className="w-8 h-8" />
          </button>
        </div>

        <button 
          onClick={() => setActiveTab('messages')}
          className={`flex flex-col items-center gap-1 transition-colors ${activeTab === 'messages' ? 'text-[#D4AF37]' : 'text-neutral-500'}`}
        >
          <MessageCircle className="w-6 h-6" />
        </button>
        <button 
          onClick={() => setActiveTab('profile')}
          className={`flex flex-col items-center gap-1 transition-colors ${activeTab === 'profile' ? 'text-[#D4AF37]' : 'text-neutral-500'}`}
        >
          <User className="w-6 h-6" />
        </button>
      </nav>
    </div>
  );
}
