import React from 'react';
import { Trophy, MapPin, QrCode, Zap, ChevronRight, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

function App() {
  const leaderboard = [
    { rank: 1, user: "RiderPTY", points: 4250, bike: "Yamaha R1" },
    { rank: 2, user: "MotoGirl_507", points: 3890, bike: "Kawasaki Ninja" },
    { rank: 3, user: "PanamaCruiser", points: 3520, bike: "Harley Iron 883" },
  ];

  return (
    <div className="min-h-screen">
      <div className="asphalt-texture"></div>

      {/* Hero Section */}
      <header className="container pt-20 pb-32">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <span className="neon-text font-bold tracking-widest text-sm mb-4 block">PANAMÁ 2026</span>
          <h1 className="text-6xl md:text-8xl mb-6 leading-tight">
            Cilindraje <span className="neon-text">507</span>
          </h1>
          <p className="text-xl text-muted max-w-2xl mx-auto mb-10 text-gray-400">
            El primer juego nacional para moteros. Recorre Panamá, escanea stickers QR en lugares épicos y compite por premios reales.
          </p>
          <div className="flex justify-center gap-4">
            <button className="btn-primary flex items-center gap-2">
              Registrar mi moto <ChevronRight size={20} />
            </button>
            <button className="px-8 py-4 rounded-full border border-white/20 font-bold hover:bg-white/5 transition-all">
              Ver Mapa
            </button>
          </div>
        </motion.div>
      </header>

      {/* How it works */}
      <section className="container py-24">
        <div className="grid md:grid-cols-3 gap-8">
          <motion.div whileHover={{ scale: 1.05 }} className="glass-card">
            <div className="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center mb-6">
              <MapPin className="text-yellow-500" />
            </div>
            <h3 className="text-xl mb-4">Explora</h3>
            <p className="text-gray-400">Encuentra stickers oficiales en miradores, talleres y puntos turísticos de todo el país.</p>
          </motion.div>

          <motion.div whileHover={{ scale: 1.05 }} className="glass-card">
            <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center mb-6">
              <QrCode className="text-orange-500" />
            </div>
            <h3 className="text-xl mb-4">Escanea</h3>
            <p className="text-gray-400">Valida tu ubicación mediante GPS y escanea el QR único para acumular puntos.</p>
          </motion.div>

          <motion.div whileHover={{ scale: 1.05 }} className="glass-card">
            <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-6">
              <Trophy className="text-blue-500" />
            </div>
            <h3 className="text-xl mb-4">Gana</h3>
            <p className="text-gray-400">Sube en el ranking nacional y participa por una moto nueva al final de la temporada.</p>
          </motion.div>
        </div>
      </section>

      {/* Leaderboard Mockup */}
      <section className="container py-24">
        <div className="glass-card max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl flex items-center gap-3">
              <Zap className="text-yellow-500" /> TOP MOTEROS
            </h2>
            <span className="text-xs bg-white/10 px-3 py-1 rounded-full">TEMPORADA 1</span>
          </div>
          <div className="space-y-4">
            {leaderboard.map((rider) => (
              <div key={rider.rank} className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 hover:border-yellow-500/30 transition-all">
                <div className="flex items-center gap-4">
                  <span className="text-2xl font-bold italic text-white/30">#{rider.rank}</span>
                  <div>
                    <p className="font-bold">{rider.user}</p>
                    <p className="text-xs text-gray-500">{rider.bike}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-yellow-500 font-bold">{rider.points} pts</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Rodada Nacional CTA */}
      <section className="container py-24 mb-20">
        <div className="bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-3xl p-12 border border-yellow-500/20 relative overflow-hidden">
          <div className="relative z-10">
            <h2 className="text-4xl mb-6">¿Listo para la <br/><span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-500 to-orange-500">Rodada Nacional?</span></h2>
            <p className="text-gray-400 mb-8 max-w-md">9 Provincias, 7 días, un solo objetivo. Demuestra que eres el motero más constante de Panamá.</p>
            <div className="flex items-center gap-6 text-sm">
              <div className="flex items-center gap-2"><ShieldCheck size={16} className="text-green-500"/> Verificado por GPS</div>
              <div className="flex items-center gap-2"><ShieldCheck size={16} className="text-green-500"/> Premios en Efectivo</div>
            </div>
          </div>
          <div className="absolute right-0 top-0 w-1/3 h-full opacity-10 flex items-center justify-center">
            <Trophy size={300} />
          </div>
        </div>
      </section>

      <footer className="container pb-10 text-center text-gray-600 text-xs uppercase tracking-widest">
        &copy; 2026 Cilindraje 507 - Jarvis Millonario Ecosystem
      </footer>
    </div>
  );
}

export default App;
