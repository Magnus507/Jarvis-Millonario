-- Esquema de Base de Datos para Cilindraje 507
-- Plataforma: Supabase (PostgreSQL)

-- 1. Perfiles de Moteros
CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  motorcycle_model TEXT,
  motorcycle_photo_url TEXT,
  total_points INTEGER DEFAULT 0,
  current_season_points INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 2. Stickers Físicos (Puntos de Interés)
CREATE TABLE stickers (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  type TEXT CHECK (type IN ('normal', 'premium', 'provincial', 'legendario')),
  points_value INTEGER NOT NULL,
  latitude DOUBLE PRECISION NOT NULL,
  longitude DOUBLE PRECISION NOT NULL,
  qr_code_key TEXT UNIQUE NOT NULL, -- El valor dentro del QR
  province TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 3. Registro de Escaneos (Check-ins)
CREATE TABLE scans (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  sticker_id UUID REFERENCES stickers(id) ON DELETE CASCADE NOT NULL,
  scan_latitude DOUBLE PRECISION,
  scan_longitude DOUBLE PRECISION,
  is_gps_valid BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
  
  -- Evitar múltiples escaneos del mismo sticker por el mismo usuario el mismo día
  UNIQUE(user_id, sticker_id, (created_at::DATE))
);

-- 4. Temporadas
CREATE TABLE seasons (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  is_active BOOLEAN DEFAULT FALSE
);
