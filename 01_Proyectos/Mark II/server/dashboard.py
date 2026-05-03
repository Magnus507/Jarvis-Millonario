from __future__ import annotations

from datetime import datetime
from typing import Any

from core.events import recent as recent_events
from core.tools import registry_summary
from memory.sqlite_store import memory_count, tool_stats


ORB_HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MARK II Orb</title>
  <style>
    :root {
      --bg: #02070b;
      --panel: rgba(3, 18, 28, 0.72);
      --cyan: #00d4ff;
      --cyan-soft: #6eeaff;
      --amber: #ff9f1a;
      --green: #00ff88;
      --red: #ff3355;
      --muted: #4d8da0;
      --text: #d8f8ff;
    }
    * { box-sizing: border-box; }
    html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }
    body {
      color: var(--text);
      font-family: "Bahnschrift", "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 50% 45%, rgba(0, 120, 180, 0.24), transparent 34%),
        radial-gradient(circle at 20% 20%, rgba(255, 130, 0, 0.10), transparent 30%),
        linear-gradient(135deg, #000306, #03111a 55%, #010407);
    }
    canvas { position: fixed; inset: 0; width: 100%; height: 100%; }
    .grain {
      pointer-events: none;
      position: fixed;
      inset: 0;
      opacity: 0.18;
      background-image:
        linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
      background-size: 44px 44px;
      mask-image: radial-gradient(circle at center, black, transparent 78%);
    }
    .hud {
      position: fixed;
      inset: 26px;
      pointer-events: none;
      display: grid;
      grid-template-columns: 310px 1fr 330px;
      grid-template-rows: auto 1fr auto;
      gap: 18px;
    }
    .panel {
      pointer-events: auto;
      border: 1px solid rgba(0, 212, 255, .32);
      background: linear-gradient(180deg, rgba(4, 22, 34, .78), rgba(2, 9, 15, .58));
      box-shadow: 0 0 34px rgba(0, 212, 255, .10), inset 0 0 30px rgba(0, 212, 255, .04);
      border-radius: 18px;
      backdrop-filter: blur(14px);
      padding: 16px;
    }
    .brand {
      grid-column: 1 / 4;
      display: flex;
      align-items: center;
      justify-content: space-between;
      letter-spacing: .16em;
      text-transform: uppercase;
    }
    .brand h1 { margin: 0; font-size: 20px; font-weight: 700; color: var(--cyan-soft); }
    .status-pill {
      border: 1px solid rgba(0, 212, 255, .45);
      border-radius: 999px;
      padding: 8px 12px;
      color: #021015;
      background: linear-gradient(90deg, var(--cyan), var(--green));
      font-weight: 800;
      letter-spacing: .12em;
      font-size: 12px;
    }
    .left { grid-column: 1; grid-row: 2; align-self: center; }
    .right { grid-column: 3; grid-row: 2; align-self: center; }
    .bottom { grid-column: 1 / 4; grid-row: 3; display: flex; justify-content: space-between; align-items: center; }
    .label { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: .18em; margin-bottom: 7px; }
    .value { color: var(--text); font-size: 16px; margin-bottom: 15px; }
    .metric { margin: 12px 0; }
    .bar { height: 7px; border: 1px solid rgba(0,212,255,.25); border-radius: 99px; overflow: hidden; background: rgba(0,0,0,.28); }
    .bar span { display: block; height: 100%; width: 50%; background: linear-gradient(90deg, var(--cyan), var(--green)); box-shadow: 0 0 18px var(--cyan); }
    .events { max-height: 250px; overflow: hidden; font-family: Consolas, monospace; font-size: 12px; color: #8ffcff; }
    .event { margin-bottom: 8px; opacity: .85; }
    .event b { color: var(--amber); }
    .link { color: var(--cyan-soft); text-decoration: none; pointer-events: auto; }
    .center-title {
      position: fixed;
      left: 50%; bottom: 15%; transform: translateX(-50%);
      text-align: center;
      letter-spacing: .28em;
      text-transform: uppercase;
      pointer-events: none;
      text-shadow: 0 0 24px rgba(0,212,255,.45);
    }
    .center-title .main { font-size: clamp(20px, 4vw, 46px); color: var(--cyan-soft); font-weight: 800; }
    .center-title .sub { margin-top: 8px; color: var(--muted); font-size: 12px; }
    @media (max-width: 900px) {
      .hud { inset: 14px; grid-template-columns: 1fr; grid-template-rows: auto auto 1fr auto; }
      .brand, .left, .right, .bottom { grid-column: 1; }
      .left { grid-row: 2; align-self: start; }
      .right { display: none; }
      .bottom { grid-row: 4; }
    }
  </style>
</head>
<body>
  <canvas id="orb"></canvas>
  <div class="grain"></div>
  <div class="center-title">
    <div class="main">MARK II</div>
    <div class="sub" id="orb-state">local neural interface</div>
  </div>
  <section class="hud">
    <div class="brand panel">
      <h1>MARK II ORB INTERFACE</h1>
      <div class="status-pill" id="status-pill">BOOTING</div>
    </div>
    <aside class="left panel">
      <div class="label">Voice Provider</div>
      <div class="value" id="voice">Gemini Live</div>
      <div class="label">Tool Registry</div>
      <div class="value"><span id="tool-count">--</span> tools online</div>
      <div class="metric"><div class="label">Core Signal</div><div class="bar"><span id="core-bar"></span></div></div>
      <div class="metric"><div class="label">Memory Index</div><div class="bar"><span id="memory-bar"></span></div></div>
      <div class="label">Links</div>
      <div class="value"><a class="link" href="/dashboard">Tool dashboard</a></div>
    </aside>
    <aside class="right panel">
      <div class="label">Recent Events</div>
      <div class="events" id="events"></div>
    </aside>
    <footer class="bottom panel">
      <span id="generated">Synchronizing...</span>
      <span>Localhost 127.0.0.1:8765</span>
    </footer>
  </section>
<script>
const canvas = document.getElementById('orb');
const ctx = canvas.getContext('2d');
const stateText = document.getElementById('orb-state');
const statusPill = document.getElementById('status-pill');
let W = 0, H = 0, DPR = 1;
let t = 0;
let currentState = 'idle';
const states = ['idle', 'listening', 'thinking', 'speaking'];
let stateIndex = 0;
let particles = [];

function resize() {
  DPR = Math.min(devicePixelRatio || 1, 2);
  W = innerWidth; H = innerHeight;
  canvas.width = Math.floor(W * DPR);
  canvas.height = Math.floor(H * DPR);
  canvas.style.width = W + 'px';
  canvas.style.height = H + 'px';
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  seedParticles();
}
addEventListener('resize', resize);

function seedParticles() {
  const count = Math.max(520, Math.min(1200, Math.floor(W * H / 1450)));
  particles = Array.from({length: count}, () => {
    const a = Math.random() * Math.PI * 2;
    const r = Math.pow(Math.random(), .58);
    return { a, r, z: Math.random(), spin: (Math.random() - .5) * .012, phase: Math.random() * 1000 };
  });
}

function stateColor() {
  if (currentState === 'speaking') return [0, 212, 255];
  if (currentState === 'thinking') return [255, 159, 26];
  if (currentState === 'listening') return [0, 255, 136];
  return [110, 234, 255];
}

function draw() {
  t += 0.016;
  ctx.clearRect(0,0,W,H);
  const cx = W / 2, cy = H / 2;
  const base = Math.min(W, H) * 0.255;
  const [cr, cg, cb] = stateColor();
  const pulse = currentState === 'speaking' ? Math.sin(t * 14) * 0.08 + 0.12 : currentState === 'thinking' ? Math.sin(t * 4) * 0.06 : 0;
  const radius = base * (1 + pulse);

  const bg = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius * 2.7);
  bg.addColorStop(0, `rgba(${cr},${cg},${cb},0.18)`);
  bg.addColorStop(.35, `rgba(${cr},${cg},${cb},0.06)`);
  bg.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = bg;
  ctx.beginPath(); ctx.arc(cx, cy, radius * 2.7, 0, Math.PI * 2); ctx.fill();

  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(t * (currentState === 'thinking' ? .18 : .06));

  for (let ring = 0; ring < 5; ring++) {
    const rr = radius * (.72 + ring * .18 + Math.sin(t * 1.3 + ring) * .012);
    ctx.strokeStyle = `rgba(${cr},${cg},${cb},${0.42 - ring * .055})`;
    ctx.lineWidth = ring === 0 ? 2.4 : 1.1;
    ctx.setLineDash([Math.max(18, rr * .16), 15 + ring * 8]);
    ctx.lineDashOffset = -t * (28 + ring * 13) * (ring % 2 ? -1 : 1);
    ctx.beginPath(); ctx.arc(0, 0, rr, 0, Math.PI * 2); ctx.stroke();
  }
  ctx.setLineDash([]);

  for (const p of particles) {
    p.a += p.spin * (currentState === 'thinking' ? 2.2 : 1);
    const wave = Math.sin(t * 1.4 + p.phase) * 0.06 + Math.cos(t * .7 + p.phase * .4) * 0.035;
    const rr = radius * (0.18 + p.r * (currentState === 'thinking' ? .95 : 1.12) + wave);
    const x = Math.cos(p.a + Math.sin(t * .2 + p.phase) * .12) * rr;
    const y = Math.sin(p.a) * rr * (.72 + p.z * .44);
    const size = (0.9 + p.z * 2.2) * (currentState === 'speaking' ? 1.25 : 1);
    const alpha = 0.16 + p.z * 0.58;
    ctx.fillStyle = `rgba(${cr},${cg},${cb},${alpha})`;
    ctx.beginPath(); ctx.arc(x, y, size, 0, Math.PI * 2); ctx.fill();
  }

  const core = ctx.createRadialGradient(0, 0, 0, 0, 0, radius * .46);
  core.addColorStop(0, `rgba(255,255,255,.98)`);
  core.addColorStop(.16, `rgba(${cr},${cg},${cb},.92)`);
  core.addColorStop(.55, `rgba(${cr},${cg},${cb},.24)`);
  core.addColorStop(1, `rgba(${cr},${cg},${cb},0)`);
  ctx.fillStyle = core;
  ctx.beginPath(); ctx.arc(0, 0, radius * .48, 0, Math.PI * 2); ctx.fill();

  ctx.strokeStyle = `rgba(255,255,255,.78)`;
  ctx.lineWidth = 1;
  for (let i = 0; i < 3; i++) {
    ctx.rotate(Math.PI / 3);
    ctx.beginPath(); ctx.moveTo(-radius * .18, 0); ctx.lineTo(radius * .18, 0); ctx.stroke();
  }
  ctx.restore();

  requestAnimationFrame(draw);
}

function setState(s) {
  currentState = s || 'idle';
  stateText.textContent = currentState.toUpperCase();
  statusPill.textContent = currentState.toUpperCase();
}

setInterval(() => {
  if (document.hidden) return;
  stateIndex = (stateIndex + 1) % states.length;
  setState(states[stateIndex]);
}, 5200);

async function refreshStatus() {
  try {
    const res = await fetch('/status', {cache: 'no-store'});
    const data = await res.json();
    document.getElementById('voice').textContent = data.voice_provider || 'Gemini Live';
    document.getElementById('tool-count').textContent = data.registry?.tool_count ?? '--';
    document.getElementById('generated').textContent = 'Updated ' + (data.generated_at || 'now');
    const mem = data.memory?.sqlite_entries ?? 0;
    document.getElementById('memory-bar').style.width = Math.min(100, 8 + mem * 8) + '%';
    document.getElementById('core-bar').style.width = Math.min(100, 45 + (data.registry?.tool_count || 0) * 2.2) + '%';
    const events = data.events || [];
    const latest = [...events].reverse().find(e => e.type === 'voice_state' || e.type === 'tool_started' || e.type === 'tool_finished' || e.type === 'task_started');
    if (latest) {
      if (latest.type === 'voice_state' && latest.payload?.state) setState(latest.payload.state);
      else if (latest.type === 'tool_started' || latest.type === 'task_started') setState('thinking');
      else if (latest.type === 'tool_finished') setState('listening');
    }
    document.getElementById('events').innerHTML = events.length
      ? events.slice(-9).reverse().map(e => `<div class="event"><b>${e.type}</b> ${JSON.stringify(e.payload).slice(0, 90)}</div>`).join('')
      : '<div class="event"><b>orb</b> waiting for MARK II events</div>';
  } catch (err) {
    statusPill.textContent = 'OFFLINE';
    stateText.textContent = 'server offline';
  }
}

resize();
setState('idle');
draw();
refreshStatus();
setInterval(refreshStatus, 2500);
</script>
</body>
</html>
"""


def build_status() -> dict[str, Any]:
    return {
        "name": "MARK II",
        "status": "online",
        "voice_provider": "Gemini Live",
        "voice_changed": False,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "registry": registry_summary(),
        "memory": {"sqlite_entries": memory_count()},
        "tools": {"stats": tool_stats(limit=20)},
        "events": recent_events(limit=25),
    }


def create_app():
    try:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse
    except Exception as exc:
        raise RuntimeError("Install fastapi and uvicorn to use the MARK II dashboard server.") from exc

    app = FastAPI(title="MARK II Orb Interface", version="0.2.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "name": "MARK II"}

    @app.get("/status")
    def status() -> dict[str, Any]:
        return build_status()

    @app.get("/events")
    def events() -> dict[str, Any]:
        return {"events": recent_events(limit=100)}

    @app.get("/", response_class=HTMLResponse)
    def orb() -> str:
        return ORB_HTML

    @app.get("/dashboard", response_class=HTMLResponse)
    def dashboard() -> str:
        data = build_status()
        tools = data["registry"]["tools"]
        rows = "".join(
            f"<tr><td>{t['name']}</td><td>{t['category']}</td><td>{t['risk']}</td><td>{t['timeout_s']}s</td></tr>"
            for t in tools
        )
        return f"""
        <!doctype html>
        <html>
        <head>
          <meta charset='utf-8'>
          <title>MARK II Dashboard</title>
          <style>
            body {{ background:#03080d; color:#d8f8ff; font-family:Consolas, monospace; margin:32px; }}
            .card {{ border:1px solid #0d3347; background:#06131d; padding:18px; margin-bottom:18px; border-radius:14px; }}
            h1 {{ color:#00d4ff; letter-spacing:2px; }}
            a {{ color:#8ffcff; }}
            table {{ width:100%; border-collapse:collapse; }}
            td, th {{ border-bottom:1px solid #12384a; padding:8px; text-align:left; }}
            .pill {{ color:#001014; background:#00d4ff; padding:3px 8px; border-radius:99px; }}
          </style>
        </head>
        <body>
          <h1>MARK II <span class='pill'>Dashboard</span></h1>
          <div class='card'><a href='/'>Back to Orb Interface</a></div>
          <div class='card'>Voice: {data['voice_provider']} | Voice changed: {data['voice_changed']}</div>
          <div class='card'>Tools: {data['registry']['tool_count']} | Memory entries: {data['memory']['sqlite_entries']}</div>
          <div class='card'><h2>Tool Registry</h2><table><tr><th>Name</th><th>Category</th><th>Risk</th><th>Timeout</th></tr>{rows}</table></div>
        </body>
        </html>
        """

    return app


app = create_app()
