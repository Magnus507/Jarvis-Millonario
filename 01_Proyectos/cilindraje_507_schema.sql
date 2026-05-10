-- Esquema de Base de Datos Estratégico para Cilindraje 507
-- Plataforma: Supabase (PostgreSQL)

-- 1. Facciones / Clubs (Equipos)
CREATE TABLE factions (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT UNIQUE NOT NULL, -- Ej: Fantasmas del West, Titanes del Interior
  description TEXT,
  banner_url TEXT,
  color_hex TEXT,
  total_points INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 2. Territorios (Provincias en Disputa)
CREATE TABLE territories (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT UNIQUE NOT NULL, -- Ej: Chiriquí, Colón, Panamá Oeste
  controlling_faction_id UUID REFERENCES factions(id),
  total_points_in_territory INTEGER DEFAULT 0,
  last_ownership_change TIMESTAMP WITH TIME ZONE
);

-- 3. Perfiles de Moteros
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  full_name TEXT,
  faction_id UUID REFERENCES factions(id), -- Pertenece a un equipo
  motorcycle_model TEXT,
  total_points INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 4. Nodos QR (Stickers Dinámicos)
CREATE TABLE stickers (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  rarity TEXT CHECK (rarity IN ('normal', 'rare', 'epic', 'legendary')),
  points_value INTEGER NOT NULL, -- 10, 50, 150, 1000
  availability_type TEXT CHECK (availability_type IN ('public', 'hidden', 'temporal', 'event', 'night')),
  active_start_time TIME, -- Para QRs nocturnos o de horarios específicos
  active_end_time TIME,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  qr_code_key TEXT UNIQUE NOT NULL,
  territory_id UUID REFERENCES territories(id),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 5. Registro de Escaneos (Check-ins) con Anti-Cheat Avanzado
CREATE TABLE scans (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  sticker_id UUID REFERENCES stickers(id) ON DELETE CASCADE NOT NULL,
  scan_latitude DOUBLE PRECISION,
  scan_longitude DOUBLE PRECISION,
  is_gps_valid BOOLEAN DEFAULT FALSE,
  device_fingerprint TEXT, -- Para detectar multi-cuentas en un mismo teléfono
  is_mock_location BOOLEAN DEFAULT FALSE, -- Detección de GPS falso
  velocity_since_last_scan FLOAT, -- Km/h desde el último escaneo (detecta teletransportación)
  flagged_for_review BOOLEAN DEFAULT FALSE, -- Si el sistema duda del escaneo
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  
  UNIQUE(user_id, sticker_id, (created_at::DATE))
);

-- 6. Temporadas
CREATE TABLE seasons (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  is_active BOOLEAN DEFAULT FALSE
);
