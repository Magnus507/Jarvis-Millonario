// Mock Data para simular la base de datos localmente antes de migrar a Supabase

export const factions = [
  { id: 'f1', name: 'Fantasmas del West', color: '#8B5CF6' }, // Violeta
  { id: 'f2', name: 'Titanes del Interior', color: '#EF4444' }, // Rojo
  { id: 'f3', name: 'Riders del Atlántico', color: '#3B82F6' }, // Azul
  { id: 'f4', name: 'Team V-Strom', color: '#F59E0B' } // Ambar
];

export const territories = [
  { id: 't1', name: 'Panamá', controlling_faction_id: 'f1', points: 15200 },
  { id: 't2', name: 'Panamá Oeste', controlling_faction_id: 'f1', points: 21400 },
  { id: 't3', name: 'Chiriquí', controlling_faction_id: 'f4', points: 18500 },
  { id: 't4', name: 'Colón', controlling_faction_id: 'f3', points: 9800 }
];

export const stickers = [
  {
    id: 's1',
    name: 'Mirador Campana',
    rarity: 'normal',
    points: 10,
    lat: 8.6854,
    lng: -79.9248,
    type: 'public',
    territory_id: 't2'
  },
  {
    id: 's2',
    name: 'QR Fantasma (Cinta Costera)',
    rarity: 'epic',
    points: 150,
    lat: 8.9774,
    lng: -79.5269,
    type: 'night',
    territory_id: 't1'
  },
  {
    id: 's3',
    name: 'Taller Moto507 (Legendario)',
    rarity: 'legendary',
    points: 1000,
    lat: 8.9824,
    lng: -79.5199,
    type: 'hidden',
    territory_id: 't1'
  }
];

export const currentUser = {
  id: 'u1',
  username: 'Rider_Alpha',
  faction_id: 'f1',
  total_points: 4250,
  provinces_visited: 3,
  scans: 12
};
