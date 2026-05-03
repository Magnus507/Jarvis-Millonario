# 🏗️ Arquitectura Técnica v1.0: Qxopa?
**Origen:** Generado por AI Studio (Gemini 1.5 Pro)
**Estado:** Planos de Ingeniería Listos

---

## 🗄️ Base de Datos (SQL para Supabase)
Este código se debe pegar en el SQL Editor de Supabase para activar la inteligencia del mapa y los filtros.

```sql
-- Activa el GPS inteligente
CREATE EXTENSION IF NOT EXISTS postgis;

-- Crea la tabla de perfiles con el Semáforo de Intenciones
CREATE TABLE profiles (
    id UUID REFERENCES auth.users PRIMARY KEY,
    username TEXT UNIQUE,
    intention_color TEXT CHECK (intention_color IN ('green', 'yellow', 'red')),
    location GEOGRAPHY(POINT),
    last_seen TIMESTAMPTZ DEFAULT NOW()
);

-- FUNCIÓN MÁGICA: Encuentra gente activa a menos de 10km con tu mismo semáforo
CREATE OR REPLACE FUNCTION get_active_matches(user_loc GEOGRAPHY, user_intent TEXT)
RETURNS SETOF profiles AS $$
BEGIN
    RETURN QUERY SELECT * FROM profiles 
    WHERE intention_color = user_intent 
    AND last_seen > NOW() - INTERVAL '60 minutes'
    AND ST_DWithin(location, user_loc, 10000);
END; $$ LANGUAGE plpgsql;
```

---

## 📱 Componentes de Interfaz (UX/UI)
- **Framework:** React + Tailwind CSS.
- **Iconografía:** Lucide React (Minimalista).
- **Animaciones:** Framer Motion (Transiciones Luxe).

## ⚡ Reglas de Oro Implementadas
1. **Filtro Real:** `last_seen < 60 mins`.
2. **Temporizador Xopa Directo:** Máximo 3 minutos por sesión.
3. **Desenfoque Progresivo:** Empieza en 40px, reduce cada 30 segundos.
