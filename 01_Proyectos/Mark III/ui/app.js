/* ── MARK III — UI Engine + Three.js Orb ─────────────────────── */

let ws = null;
let scene, camera, renderer, orb, particles, clock;
let currentState = 'idle';
const STATE_COLORS = {
  idle:      { core: 0x0044ff, glow: 0x0088ff, particles: 0x00aaff },
  listening: { core: 0x00cc66, glow: 0x00ff88, particles: 0x00ffaa },
  thinking:  { core: 0xff8800, glow: 0xffaa00, particles: 0xffcc44 },
  speaking:  { core: 0x0088ff, glow: 0x00ccff, particles: 0x44eeff },
  error:     { core: 0xff2222, glow: 0xff4444, particles: 0xff6666 },
};

/* ── WebSocket ────────────────────────────────────────────────── */
function connectWS() {
  const host = window.location.host;
  ws = new WebSocket(`ws://${host}/ws`);

  ws.onopen = () => {
    addLog('Conexión establecida', 'success');
    ws.send(JSON.stringify({ action: 'settings_get' }));
    loadTools();
  };

  ws.onmessage = ({ data }) => {
    const msg = JSON.parse(data);
    handleEvent(msg);
  };

  ws.onclose = () => {
    addLog('Conexión perdida — reconectando...', 'warn');
    setTimeout(connectWS, 2000);
  };

  ws.onerror = () => addLog('Error de WebSocket', 'error');
}

function send(action, extra = {}) {
  if (ws && ws.readyState === WebSocket.OPEN)
    ws.send(JSON.stringify({ action, ...extra }));
}

/* ── Event Handler ────────────────────────────────────────────── */
function handleEvent(msg) {
  switch (msg.type) {
    case 'state_change':
      setState(msg.state);
      break;

    case 'message':
      if (msg.role === 'user')     addMessage(msg.text, 'user');
      else if (msg.role === 'assistant') addMessage(msg.text, 'assistant');
      break;

    case 'tool_start':
      addLog(`⚙ ${msg.tool}`, 'warn');
      showToolBadge(msg.tool);
      break;

    case 'tool_end':
      hideToolBadge();
      addLog(`✓ ${msg.tool}`, 'success');
      break;

    case 'error':
      setState('error');
      addMessage(`Error: ${msg.message}`, 'system');
      addLog(msg.message, 'error');
      break;

    case 'settings':
      document.getElementById('provider-badge').textContent = msg.provider.toUpperCase();
      break;
  }
}

/* ── State Management ─────────────────────────────────────────── */
function setState(state) {
  currentState = state;
  document.body.setAttribute('data-state', state);
  document.getElementById('state-label').textContent = STATE_LABELS[state] || state;
  updateOrbState(state);
}

const STATE_LABELS = {
  idle:      'EN ESPERA',
  listening: 'ESCUCHANDO',
  thinking:  'PROCESANDO',
  speaking:  'RESPONDIENDO',
  error:     'ERROR',
};

/* ── Messages ─────────────────────────────────────────────────── */
function addMessage(text, role) {
  const container = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = `msg ${role}`;

  if (role !== 'system') {
    const header = document.createElement('div');
    header.className = 'msg-header';
    header.textContent = role === 'user' ? '▶ TÚ' : '◆ MARK';
    div.appendChild(header);
  }

  const content = document.createElement('div');
  content.textContent = text;
  div.appendChild(content);
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function showToolBadge(toolName) {
  let badge = document.getElementById('tool-badge');
  if (!badge) {
    badge = document.createElement('div');
    badge.id = 'tool-badge';
    badge.className = 'msg system';
    badge.innerHTML = `<span class="tool-badge">⚙ <span id="tool-name"></span></span>`;
    document.getElementById('messages').appendChild(badge);
  }
  document.getElementById('tool-name').textContent = toolName;
  document.getElementById('messages').scrollTop = 999999;
}

function hideToolBadge() {
  const badge = document.getElementById('tool-badge');
  if (badge) badge.remove();
}

/* ── Input ────────────────────────────────────────────────────── */
function sendMessage() {
  const box = document.getElementById('input-box');
  const text = box.value.trim();
  if (!text) return;
  box.value = '';
  box.style.height = '48px';
  addMessage(text, 'user');
  send('chat', { text });
}

/* ── Activity Log ─────────────────────────────────────────────── */
function addLog(text, type = '') {
  const log = document.getElementById('activity-log');
  const now = new Date().toLocaleTimeString('es', { hour12: false });
  const div = document.createElement('div');
  div.className = `log-entry ${type}`;
  div.textContent = `[${now}] ${text}`;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
  if (log.children.length > 100) log.removeChild(log.firstChild);
}

/* ── Tools List ───────────────────────────────────────────────── */
async function loadTools() {
  try {
    const r = await fetch('/api/tools');
    const { tools } = await r.json();
    const list = document.getElementById('tools-list');
    const cats = {};
    tools.forEach(t => {
      if (!cats[t.category]) cats[t.category] = [];
      cats[t.category].push(t);
    });
    list.innerHTML = Object.entries(cats).map(([cat, ts]) =>
      `<div style="color:var(--text-dim);margin-top:4px">${cat}</div>` +
      ts.map(t => `<div class="tool-name">· ${t.name}</div>`).join('')
    ).join('');
  } catch (e) { /* server not ready yet */ }
}

/* ══════════════════════════════════════════════════════════════ */
/* ── THREE.JS ORB ─────────────────────────────────────────────── */
/* ══════════════════════════════════════════════════════════════ */

function initOrb() {
  const canvas = document.getElementById('orb-canvas');

  // Scene
  scene = new THREE.Scene();
  clock = new THREE.Clock();

  // Camera
  camera = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
  camera.position.z = 2.8;

  // Renderer
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(340, 340);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 0);

  _buildOrb();
  _buildParticles();
  _buildArcs();
  _buildRings();

  animate();
}

function _buildOrb() {
  const geo = new THREE.SphereGeometry(1, 64, 64);
  const mat = new THREE.MeshPhongMaterial({
    color: 0x0044ff,
    emissive: 0x001133,
    transparent: true,
    opacity: 0.15,
    wireframe: false,
  });
  orb = new THREE.Mesh(geo, mat);
  scene.add(orb);

  // Wireframe layer
  const wireMat = new THREE.MeshBasicMaterial({
    color: 0x0088ff,
    wireframe: true,
    transparent: true,
    opacity: 0.08,
  });
  const wire = new THREE.Mesh(geo, wireMat);
  wire.scale.setScalar(1.01);
  scene.add(wire);

  // Glow sphere (bigger, very transparent)
  const glowGeo = new THREE.SphereGeometry(1.15, 32, 32);
  const glowMat = new THREE.MeshBasicMaterial({
    color: 0x0066ff,
    transparent: true,
    opacity: 0.06,
    side: THREE.BackSide,
  });
  const glow = new THREE.Mesh(glowGeo, glowMat);
  scene.add(glow);
  orb._glow = glow;
  orb._wire = wire;

  // Lighting
  const ambient = new THREE.AmbientLight(0x001133, 1.2);
  scene.add(ambient);

  const pLight = new THREE.PointLight(0x0088ff, 3, 8);
  pLight.position.set(2, 2, 2);
  scene.add(pLight);
  orb._light = pLight;
}

function _buildParticles() {
  const COUNT = 1800;
  const positions = new Float32Array(COUNT * 3);
  const scales = new Float32Array(COUNT);

  for (let i = 0; i < COUNT; i++) {
    const r = 1.05 + Math.random() * 0.6;
    const phi = Math.acos(-1 + (2 * i) / COUNT);
    const theta = Math.sqrt(COUNT * Math.PI) * phi + Math.random() * 0.4;
    positions[i * 3]     = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);
    scales[i] = Math.random();
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('aScale', new THREE.BufferAttribute(scales, 1));

  const mat = new THREE.PointsMaterial({
    color: 0x00aaff,
    size: 0.022,
    transparent: true,
    opacity: 0.75,
    sizeAttenuation: true,
  });

  particles = new THREE.Points(geo, mat);
  scene.add(particles);
}

function _buildArcs() {
  orb._arcs = [];
  for (let i = 0; i < 3; i++) {
    const curve = new THREE.EllipseCurve(
      0, 0, 1.1 + i * 0.05, 1.1 + i * 0.05,
      0, Math.PI * 2, false, (i * Math.PI) / 3
    );
    const points = curve.getPoints(80);
    const geo = new THREE.BufferGeometry().setFromPoints(points);
    const mat = new THREE.LineBasicMaterial({
      color: 0x0088ff,
      transparent: true,
      opacity: 0.12 - i * 0.03,
    });
    const arc = new THREE.Line(geo, mat);
    arc.rotation.x = Math.random() * Math.PI;
    arc.rotation.y = Math.random() * Math.PI;
    scene.add(arc);
    orb._arcs.push(arc);
  }
}

function _buildRings() {
  orb._rings = [];
  for (let i = 0; i < 2; i++) {
    const geo = new THREE.TorusGeometry(1.2 + i * 0.12, 0.004, 8, 100);
    const mat = new THREE.MeshBasicMaterial({
      color: 0x0066ff,
      transparent: true,
      opacity: 0.2 - i * 0.06,
    });
    const ring = new THREE.Mesh(geo, mat);
    ring.rotation.x = Math.PI / 2 + i * 0.6;
    ring.rotation.y = i * 0.8;
    scene.add(ring);
    orb._rings.push(ring);
  }
}

function updateOrbState(state) {
  const colors = STATE_COLORS[state] || STATE_COLORS.idle;

  if (orb) {
    orb.material.color.setHex(colors.core);
    orb._glow.material.color.setHex(colors.glow);
    orb._light.color.setHex(colors.glow);
  }
  if (particles) {
    particles.material.color.setHex(colors.particles);
  }
}

function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  if (orb) {
    const scale = currentState === 'thinking'
      ? 1 + Math.sin(t * 4) * 0.04
      : currentState === 'speaking'
      ? 1 + Math.sin(t * 8) * 0.06
      : 1 + Math.sin(t * 1.2) * 0.012;

    orb.scale.setScalar(scale);
    orb.rotation.y = t * 0.2;
    orb.rotation.x = Math.sin(t * 0.3) * 0.15;

    orb._glow.scale.setScalar(scale * 1.05);
    orb._wire.rotation.y = -t * 0.15;

    orb._arcs.forEach((arc, i) => {
      arc.rotation.z = t * (0.4 + i * 0.15);
      arc.rotation.x = Math.sin(t * 0.5 + i) * 0.4;
    });

    orb._rings.forEach((ring, i) => {
      ring.rotation.z = t * (0.25 + i * 0.1);
      ring.material.opacity = 0.15 + Math.sin(t * 2 + i) * 0.08;
    });
  }

  if (particles) {
    particles.rotation.y = t * 0.08;
    particles.rotation.x = Math.sin(t * 0.2) * 0.05;

    const speed = currentState === 'idle' ? 0.08
      : currentState === 'thinking' ? 0.35
      : currentState === 'speaking' ? 0.25
      : 0.15;

    const pos = particles.geometry.attributes.position.array;
    for (let i = 0; i < pos.length; i += 3) {
      const ix = i / 3;
      pos[i + 1] += Math.sin(t * speed + ix * 0.5) * 0.0008;
    }
    particles.geometry.attributes.position.needsUpdate = true;
  }

  renderer.render(scene, camera);
}

/* ── Init ─────────────────────────────────────────────────────── */
window.addEventListener('DOMContentLoaded', () => {
  // Load Three.js dynamically
  const script = document.createElement('script');
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js';
  script.onload = () => {
    initOrb();
    connectWS();
    setState('idle');
    addMessage('MARK III activo. Di "Hola Mark" o escribe un comando.', 'system');
    addLog('Sistema iniciado', 'success');
  };
  document.head.appendChild(script);

  // Input handlers
  const box = document.getElementById('input-box');
  box.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  box.addEventListener('input', () => {
    box.style.height = '48px';
    box.style.height = Math.min(box.scrollHeight, 150) + 'px';
  });

  document.getElementById('send-btn').addEventListener('click', sendMessage);
  document.getElementById('reset-btn').addEventListener('click', () => {
    send('reset');
    document.getElementById('messages').innerHTML = '';
    addMessage('Conversación reiniciada.', 'system');
  });
});
