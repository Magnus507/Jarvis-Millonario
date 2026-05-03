# 🚀 Master Prompt: Qxopa? App Generator
**Instrucciones:** Copia y pega este prompt íntegro en Google AI Studio (Gemini 1.5 Pro) para generar la estructura, el código y el esquema de base de datos.

---

## CONTEXTO DEL SISTEMA
Eres un Ingeniero de Software Senior y Arquitecto de Producto especializado en el mercado de Panamá. Estás desarrollando el MVP de **Qxopa?**, una aplicación de conexión social y citas que prioriza "Planes sobre Perfiles".

## STACK TÉCNICO RECOMENDADO
- **Frontend:** React Native (Expo) con Tailwind CSS (NativeWind).
- **Backend/Almacenamiento:** Supabase (PostgreSQL, Auth, Storage y Real-time). Es crucial usar Supabase por su capa gratuita y manejo de WebSockets para el video-chat.
- **Video:** WebRTC o integración con Daily.co para el módulo Omegle.

## CORE LOGIC (REGLAS DE NEGOCIO)
1. **Filtro de Actividad:** Solo son visibles usuarios con actividad (`last_seen`) menor a 60 minutos.
2. **Semáforo de Intenciones:** Los usuarios se agrupan por 🟢 (Social), 🟡 (Dating), 🔴 (Action). Solo hay match entre colores iguales.
3. **Xopa Directo (Módulo Omegle):** Video-chat aleatorio de 3 minutos filtrado por Geofencing (radio de 10km) y Semáforo.
4. **Privacidad:** Implementar un filtro de `blur` progresivo en el componente de video que se aclara cada 30 segundos.

## ESQUEMA DE BASE DE DATOS (SUPABASE)
Genera el SQL para las siguientes tablas:
- `profiles`: id, username, age, bio, intention_color, avatar_url, last_seen, location (PostGIS), karma_points.
- `plans`: id, creator_id, local_id (FK), description, start_time, status (active/expired).
- `matches`: id, user1_id, user2_id, type (plan_match / xopa_direct), created_at.
- `local_partners`: id, name, category, coordinates, discount_code.

## REQUERIMIENTOS DE UI/UX (ESTÉTICA LUXE)
- **Paleta de Colores:** Negro Profundo, Dorado (Luxe), y los colores del semáforo (Verde Neón, Amarillo Vibrante, Rojo Sangre).
- **Tipografía:** Moderna, sin serifa (estilo Inter o Montserrat).
- **Componentes:**
    - Mapa interactivo de Panamá con pines de locales aliados.
    - Botón central flotante de "Xopa Directo" con animación de pulso.
    - Feed de "Parkings" estilo tarjetas minimalistas.

## TAREA ESPECÍFICA
Genera el código inicial para:
1. El esquema de base de datos SQL para Supabase.
2. El componente principal de navegación (Bottom Tabs).
3. La lógica del "Semáforo de Intenciones" que filtra los perfiles en tiempo real.
4. Un prototipo funcional del componente "Xopa Directo" con el temporizador de 3 minutos.

---
*Fin del Prompt*
