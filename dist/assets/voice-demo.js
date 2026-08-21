/* FROM FUTURE — custom voice demo widget.
   Fully custom touch-to-talk client for ElevenLabs Conversational AI —
   connects straight to the public conversation WebSocket (no embed, no
   third-party widget UI). Mic audio is downsampled to PCM16 and streamed
   up; agent audio streams back as PCM16 chunks and is scheduled through
   Web Audio. */
(function () {
  var cfg = window.FF_VOICE_DEMO;
  if (!cfg) return;
  var stage = document.getElementById(cfg.stageId || 'vdStage');
  if (!stage) return;

  var WS_BASE = 'wss://api.us.elevenlabs.io/v1/convai/conversation?agent_id=';
  var orb = document.getElementById('vdOrb');
  var statusEl = document.getElementById('vdStatus');
  var captionEl = document.getElementById('vdCaption');
  var pills = Array.prototype.slice.call(stage.querySelectorAll('.vd-pill'));
  var svg = document.getElementById('vdTentacles');

  var state = {
    agent: null, pill: null,
    ws: null, ac: null, stream: null, proc: null, src: null,
    playCursor: 0, sources: [], live: false, connecting: false,
    inRate: 16000, outRate: 16000
  };

  /* ---------- tentacle drawing ---------- */
  function drawTentacles() {
    if (!svg) return;
    var sw = stage.clientWidth, sh = stage.clientHeight;
    if (sw < 40) return;
    svg.setAttribute('viewBox', '0 0 ' + sw + ' ' + sh);
    var srect = stage.getBoundingClientRect();
    var orect = orb.getBoundingClientRect();
    var ox = orect.left - srect.left + orect.width / 2;
    var oy = orect.top - srect.top + orect.height / 2;
    var paths = '';
    pills.forEach(function (p, i) {
      var r = p.getBoundingClientRect();
      var px = r.left - srect.left + r.width / 2;
      var py = r.top - srect.top + r.height / 2;
      /* start at pill edge nearest orb */
      var toOrbX = ox - px, toOrbY = oy - py;
      var sx = px + (toOrbX > 0 ? r.width / 2 : -r.width / 2);
      var sy = py;
      var ex = ox + (toOrbX > 0 ? -66 : 66) * 0.92;
      var ey = oy + (toOrbY > 0 ? -30 : 30);
      /* octopus curl: control points bow outward */
      var mx = (sx + ex) / 2, my = (sy + ey) / 2;
      var bow = (i % 2 === 0 ? -1 : 1) * (36 + i * 10);
      var c1x = sx + (mx - sx) * 0.5, c1y = sy + bow;
      var c2x = ex - (ex - mx) * 0.5, c2y = ey - bow * 0.6;
      var act = (state.pill === p) ? ' vd-t-active' : '';
      paths += '<path class="vd-t' + act + '" d="M' + sx.toFixed(1) + ' ' + sy.toFixed(1) +
        ' C' + c1x.toFixed(1) + ' ' + c1y.toFixed(1) + ', ' + c2x.toFixed(1) + ' ' + c2y.toFixed(1) +
        ', ' + ex.toFixed(1) + ' ' + ey.toFixed(1) + '"/>' +
        '<circle class="vd-dot' + act + '" cx="' + sx.toFixed(1) + '" cy="' + sy.toFixed(1) + '" r="3.5"/>' +
        '<circle class="vd-dot' + act + '" cx="' + ex.toFixed(1) + '" cy="' + ey.toFixed(1) + '" r="3.5"/>';
    });
    svg.innerHTML =
      '<defs><linearGradient id="vdGrad" x1="0%" y1="0%" x2="100%" y2="0%">' +
      '<stop offset="0%" stop-color="#6366f1"/><stop offset="55%" stop-color="#a855f7"/>' +
      '<stop offset="100%" stop-color="#fcd34d"/></linearGradient></defs>' + paths;
  }
  window.addEventListener('resize', drawTentacles);

  /* ---------- audio helpers ---------- */
  function b64ToI16(b64) {
    var bin = atob(b64), n = bin.length, bytes = new Uint8Array(n);
    for (var i = 0; i < n; i++) bytes[i] = bin.charCodeAt(i);
    return new Int16Array(bytes.buffer);
  }
  function f32ToB64I16(f32) {
    var i16 = new Int16Array(f32.length);
    for (var i = 0; i < f32.length; i++) {
      var s = Math.max(-1, Math.min(1, f32[i]));
      i16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
    }
    var bytes = new Uint8Array(i16.buffer), bin = '';
    for (var j = 0; j < bytes.length; j += 8192)
      bin += String.fromCharCode.apply(null, bytes.subarray(j, j + 8192));
    return btoa(bin);
  }
  function downsample(f32, fromRate, toRate) {
    if (fromRate === toRate) return f32;
    var ratio = fromRate / toRate, outLen = Math.floor(f32.length / ratio);
    var out = new Float32Array(outLen);
    for (var i = 0; i < outLen; i++) {
      var lo = Math.floor(i * ratio), hi = Math.min(Math.floor((i + 1) * ratio), f32.length);
      var sum = 0, c = 0;
      for (var k = lo; k < hi; k++) { sum += f32[k]; c++; }
      out[i] = c ? sum / c : 0;
    }
    return out;
  }
  function parseRate(fmt, fallback) {
    var m = /(\d{4,6})/.exec(fmt || '');
    return m ? parseInt(m[1], 10) : fallback;
  }
  function playChunk(i16) {
    var ac = state.ac;
    if (!ac) return;
    var f32 = new Float32Array(i16.length);
    for (var i = 0; i < i16.length; i++) f32[i] = i16[i] / 32768;
    var buf = ac.createBuffer(1, f32.length, state.outRate);
    buf.copyToChannel(f32, 0);
    var s = ac.createBufferSource();
    s.buffer = buf; s.connect(ac.destination);
    var now = ac.currentTime;
    if (state.playCursor < now + 0.06) state.playCursor = now + 0.06;
    s.start(state.playCursor);
    state.playCursor += buf.duration;
    state.sources.push(s);
    s.onended = function () {
      var ix = state.sources.indexOf(s);
      if (ix > -1) state.sources.splice(ix, 1);
      if (!state.sources.length) orb.classList.remove('vd-speaking');
    };
    orb.classList.add('vd-speaking');
  }
  function flushPlayback() {
    state.sources.forEach(function (s) { try { s.stop(); } catch (e) {} });
    state.sources = [];
    state.playCursor = 0;
    orb.classList.remove('vd-speaking');
  }

  /* ---------- session ---------- */
  function setStatus(t) { if (statusEl) statusEl.textContent = t; }
  function setCaption(t) { if (captionEl) captionEl.textContent = t || ''; }

  function stop(msg) {
    state.live = false; state.connecting = false;
    if (state.ws) { try { state.ws.close(); } catch (e) {} state.ws = null; }
    if (state.proc) { try { state.proc.disconnect(); } catch (e) {} state.proc = null; }
    if (state.src) { try { state.src.disconnect(); } catch (e) {} state.src = null; }
    if (state.stream) { state.stream.getTracks().forEach(function (t) { t.stop(); }); state.stream = null; }
    flushPlayback();
    if (state.ac) { try { state.ac.close(); } catch (e) {} state.ac = null; }
    orb.classList.remove('vd-live', 'vd-connecting', 'vd-speaking');
    setStatus(msg || (state.agent ? 'Tap to talk to ' + state.agent.label : 'Pick a demo, then tap to talk'));
    setCaption('');
  }

  function start() {
    if (!state.agent) { setStatus('Pick a demo first ↑'); return; }
    if (state.connecting) return;
    state.connecting = true;
    orb.classList.add('vd-connecting');
    setStatus('Connecting…');
    navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } })
      .then(function (stream) {
        state.stream = stream;
        var AC = window.AudioContext || window.webkitAudioContext;
        state.ac = new AC();
        var ws = new WebSocket(WS_BASE + encodeURIComponent(state.agent.id));
        state.ws = ws;
        ws.onopen = function () {
          ws.send(JSON.stringify({ type: 'conversation_initiation_client_data' }));
        };
        ws.onmessage = function (ev) {
          var d;
          try { d = JSON.parse(ev.data); } catch (e) { return; }
          switch (d.type) {
            case 'conversation_initiation_metadata':
              var md = d.conversation_initiation_metadata_event || {};
              state.outRate = parseRate(md.agent_output_audio_format, 16000);
              state.inRate = parseRate(md.user_input_audio_format, 16000);
              beginMicPump();
              state.connecting = false; state.live = true;
              orb.classList.remove('vd-connecting');
              orb.classList.add('vd-live');
              setStatus('Live — speak naturally. Tap to end.');
              break;
            case 'audio':
              if (d.audio_event && d.audio_event.audio_base_64) playChunk(b64ToI16(d.audio_event.audio_base_64));
              break;
            case 'interruption':
              flushPlayback();
              break;
            case 'agent_response':
              var ar = d.agent_response_event;
              if (ar && ar.agent_response) setCaption(ar.agent_response);
              break;
            case 'ping':
              var pe = d.ping_event || {};
              ws.send(JSON.stringify({ type: 'pong', event_id: pe.event_id }));
              break;
          }
        };
        ws.onerror = function () { stop('Connection hiccup — tap to retry'); };
        ws.onclose = function () { if (state.live || state.connecting) stop(); };
      })
      .catch(function () {
        state.connecting = false;
        orb.classList.remove('vd-connecting');
        setStatus('Microphone blocked — allow mic access and tap again');
      });
  }

  function beginMicPump() {
    var ac = state.ac, stream = state.stream, ws = state.ws;
    if (!ac || !stream || !ws) return;
    if (ac.state === 'suspended') ac.resume();
    state.src = ac.createMediaStreamSource(stream);
    state.proc = ac.createScriptProcessor(4096, 1, 1);
    state.proc.onaudioprocess = function (e) {
      if (!state.live || !state.ws || state.ws.readyState !== 1) return;
      var ds = downsample(e.inputBuffer.getChannelData(0), ac.sampleRate, state.inRate);
      state.ws.send(JSON.stringify({ user_audio_chunk: f32ToB64I16(ds) }));
    };
    state.src.connect(state.proc);
    state.proc.connect(ac.destination); /* required by some browsers; outputs silence */
  }

  /* ---------- wiring ---------- */
  pills.forEach(function (p) {
    p.addEventListener('click', function () {
      var wasLive = state.live || state.connecting;
      if (wasLive) stop();
      pills.forEach(function (x) { x.classList.remove('vd-active'); });
      p.classList.add('vd-active');
      state.pill = p;
      state.agent = { id: p.getAttribute('data-agent'), label: p.getAttribute('data-label') || p.textContent.trim() };
      drawTentacles();
      setStatus('Tap the orb to talk to ' + state.agent.label);
      if (wasLive) start();
    });
  });
  orb.addEventListener('click', function () {
    if (state.live || state.connecting) stop(); else start();
  });

  /* default selection: first pill (Kotton From Future) */
  if (pills.length) {
    pills[0].classList.add('vd-active');
    state.pill = pills[0];
    state.agent = { id: pills[0].getAttribute('data-agent'), label: pills[0].getAttribute('data-label') || pills[0].textContent.trim() };
  }
  drawTentacles();
  /* fonts/layout settle */
  setTimeout(drawTentacles, 400);
  setTimeout(drawTentacles, 1500);
})();
