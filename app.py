HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Curseflow</title>
  <style>
    :root {
      --bg: #f7f8f2;
      --ink: #171717;
      --muted: #5f6460;
      --panel: #ffffff;
      --line: #d9ded6;
      --accent: #146c54;
      --accent-2: #d84f2a;
      --accent-3: #2156a5;
      --soft: #ecf3ed;
      --shadow: 0 18px 48px rgba(23, 23, 23, 0.12);
    }

    * {
      box-sizing: border-box;
    }

    html,
    body {
      margin: 0;
      min-height: 100%;
      font-family: "Aptos", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(20, 108, 84, 0.08) 1px, transparent 1px),
        linear-gradient(rgba(20, 108, 84, 0.08) 1px, transparent 1px),
        var(--bg);
      background-size: 36px 36px;
    }

    body {
      padding: 18px;
      cursor: none;
    }

    button,
    .gesture-target {
      cursor: none;
    }

    .app {
      min-height: calc(100vh - 36px);
      display: grid;
      grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
      gap: 18px;
    }

    .sidebar,
    .stage {
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.88);
      box-shadow: var(--shadow);
    }

    .sidebar {
      display: flex;
      flex-direction: column;
      gap: 18px;
      padding: 18px;
      border-radius: 8px;
    }

    .brand {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--line);
    }

    h1 {
      margin: 0;
      font-size: 30px;
      line-height: 1.05;
      letter-spacing: 0;
    }

    .pill {
      min-width: 92px;
      padding: 8px 10px;
      border-radius: 999px;
      color: #fff;
      text-align: center;
      font-size: 13px;
      font-weight: 700;
      background: var(--accent-2);
    }

    .pill.live {
      background: var(--accent);
    }

    .controls {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    button {
      min-height: 44px;
      border: 1px solid transparent;
      border-radius: 8px;
      padding: 10px 12px;
      font: inherit;
      font-weight: 700;
      color: #fff;
      background: var(--accent);
      transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }

    button:hover,
    .gesture-target.hovered {
      transform: translateY(-1px);
      box-shadow: 0 8px 20px rgba(20, 108, 84, 0.18);
    }

    button.secondary {
      color: var(--ink);
      border-color: var(--line);
      background: #fff;
    }

    button:disabled {
      opacity: 0.52;
      transform: none;
      box-shadow: none;
    }

    .preview {
      position: relative;
      aspect-ratio: 4 / 3;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #111;
    }

    video,
    canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transform: scaleX(-1);
    }

    video {
      display: none;
    }

    .metrics {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .metric {
      min-height: 78px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--soft);
    }

    .metric span {
      display: block;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }

    .metric strong {
      display: block;
      font-size: 20px;
      line-height: 1.1;
      word-break: break-word;
    }

    .log {
      min-height: 74px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--muted);
      background: #fff;
      font-size: 14px;
      line-height: 1.5;
    }

    .stage {
      position: relative;
      overflow: hidden;
      border-radius: 8px;
      padding: 18px;
      display: grid;
      grid-template-rows: auto 1fr;
      gap: 18px;
    }

    .toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 14px;
    }

    .toolbar h2 {
      margin: 0;
      font-size: 22px;
      letter-spacing: 0;
    }

    .click-count {
      color: var(--muted);
      font-weight: 700;
    }

    .workspace {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      align-content: start;
    }

    .gesture-target {
      min-height: 160px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      background: #fff;
      transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
    }

    .gesture-target.clicked {
      border-color: var(--accent-3);
      box-shadow: 0 0 0 4px rgba(33, 86, 165, 0.18);
    }

    .gesture-target h3 {
      margin: 0 0 10px;
      font-size: 22px;
      letter-spacing: 0;
    }

    .gesture-target p {
      margin: 0;
      color: var(--muted);
      line-height: 1.45;
    }

    .target-a {
      border-top: 8px solid var(--accent);
    }

    .target-b {
      border-top: 8px solid var(--accent-2);
    }

    .target-c {
      border-top: 8px solid var(--accent-3);
    }

    .cursor {
      position: fixed;
      z-index: 50;
      left: 0;
      top: 0;
      width: 34px;
      height: 34px;
      border: 3px solid #fff;
      border-radius: 50%;
      background: rgba(20, 108, 84, 0.78);
      box-shadow: 0 0 0 2px rgba(20, 108, 84, 0.9), 0 12px 24px rgba(0, 0, 0, 0.22);
      pointer-events: none;
      opacity: 0;
      transform: translate(-50%, -50%);
      transition: opacity 120ms ease, width 120ms ease, height 120ms ease, background 120ms ease;
    }

    .cursor.active {
      opacity: 1;
    }

    .cursor.clicking {
      width: 48px;
      height: 48px;
      background: rgba(216, 79, 42, 0.85);
    }

    @media (max-width: 960px) {
      body {
        padding: 10px;
      }

      .app {
        min-height: calc(100vh - 20px);
        grid-template-columns: 1fr;
      }

      .workspace {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <main class="app">
    <aside class="sidebar">
      <div class="brand">
        <h1>Curseflow</h1>
        <div id="statusPill" class="pill">Idle</div>
      </div>
      <div class="controls">
        <button id="activateBtn" type="button">Activate</button>
        <button id="stopBtn" class="secondary" type="button" disabled>Stop</button>
      </div>
      <div class="preview">
        <video id="cameraFeed" autoplay playsinline muted></video>
        <canvas id="overlay"></canvas>
      </div>
      <section class="metrics">
        <div class="metric">
          <span>Hand</span>
          <strong id="handState">Waiting</strong>
        </div>
        <div class="metric">
          <span>Face</span>
          <strong id="faceState">Waiting</strong>
        </div>
        <div class="metric">
          <span>Gesture</span>
          <strong id="gestureState">None</strong>
        </div>
        <div class="metric">
          <span>Clicks</span>
          <strong id="clickCount">0</strong>
        </div>
      </section>
      <div id="eventLog" class="log">Activate camera to start gesture tracking.</div>
    </aside>

    <section class="stage">
      <div class="toolbar">
        <h2>Gesture Workspace</h2>
        <div class="click-count" id="lastAction">No action yet</div>
      </div>
      <div class="workspace">
        <button class="gesture-target target-a" type="button" data-label="Launch Pad">
          <h3>Launch Pad</h3>
          <p>Move the pointer here with your index finger and double blink to trigger it.</p>
        </button>
        <button class="gesture-target target-b" type="button" data-label="Focus Mode">
          <h3>Focus Mode</h3>
          <p>This target proves gesture clicks are routed to real page controls.</p>
        </button>
        <button class="gesture-target target-c" type="button" data-label="Control Check">
          <h3>Control Check</h3>
          <p>Use it as a test area after the webcam model finishes loading.</p>
        </button>
      </div>
    </section>
  </main>
  <div id="gestureCursor" class="cursor"></div>

  <script type="module">
    import {
      FilesetResolver,
      FaceLandmarker,
      HandLandmarker
    } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22";

    const activateBtn = document.getElementById("activateBtn");
    const stopBtn = document.getElementById("stopBtn");
    const statusPill = document.getElementById("statusPill");
    const cameraFeed = document.getElementById("cameraFeed");
    const overlay = document.getElementById("overlay");
    const overlayCtx = overlay.getContext("2d");
    const handState = document.getElementById("handState");
    const faceState = document.getElementById("faceState");
    const gestureState = document.getElementById("gestureState");
    const clickCountEl = document.getElementById("clickCount");
    const eventLog = document.getElementById("eventLog");
    const lastAction = document.getElementById("lastAction");
    const gestureCursor = document.getElementById("gestureCursor");

    const leftEyeIdx = [33, 160, 158, 133, 153, 144];
    const rightEyeIdx = [362, 385, 387, 263, 373, 380];

    let stream = null;
    let running = false;
    let vision = null;
    let faceLandmarker = null;
    let handLandmarker = null;
    let animationId = null;
    let lastVideoTime = -1;
    let smoothX = null;
    let smoothY = null;
    let closedFrames = 0;
    let pendingBlinks = 0;
    let lastShortBlink = 0;
    let lastLeftClick = 0;
    let clickCount = 0;
    let hoveredElement = null;

    const smoothing = 0.28;
    const eyeCloseThreshold = 0.21;
    const shortBlinkFrames = 2;
    const longBlinkFrames = 8;
    const doubleBlinkWindow = 700;
    const clickCooldown = 450;

    function setLog(message) {
      eventLog.textContent = message;
    }

    function setStatus(label, live = false) {
      statusPill.textContent = label;
      statusPill.classList.toggle("live", live);
    }

    function dist(a, b) {
      return Math.hypot(a.x - b.x, a.y - b.y);
    }

    function eyeAspectRatio(landmarks, idx) {
      const p1 = landmarks[idx[0]];
      const p2 = landmarks[idx[1]];
      const p3 = landmarks[idx[2]];
      const p4 = landmarks[idx[3]];
      const p5 = landmarks[idx[4]];
      const p6 = landmarks[idx[5]];
      const vertical = dist(p2, p6) + dist(p3, p5);
      const horizontal = 2 * dist(p1, p4);
      return horizontal === 0 ? 0 : vertical / horizontal;
    }

    async function loadModels() {
      if (faceLandmarker && handLandmarker) {
        return;
      }

      setStatus("Loading");
      setLog("Loading browser gesture models...");
      vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22/wasm"
      );

      handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath: "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
          delegate: "GPU"
        },
        runningMode: "VIDEO",
        numHands: 1,
        minHandDetectionConfidence: 0.65,
        minHandPresenceConfidence: 0.55,
        minTrackingConfidence: 0.55
      });

      faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath: "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
          delegate: "GPU"
        },
        runningMode: "VIDEO",
        numFaces: 1,
        minFaceDetectionConfidence: 0.55,
        minFacePresenceConfidence: 0.5,
        minTrackingConfidence: 0.5
      });
    }

    function resizeOverlay() {
      const rect = overlay.getBoundingClientRect();
      const ratio = window.devicePixelRatio || 1;
      overlay.width = Math.max(1, Math.floor(rect.width * ratio));
      overlay.height = Math.max(1, Math.floor(rect.height * ratio));
      overlayCtx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function drawHandPoint(point) {
      const rect = overlay.getBoundingClientRect();
      overlayCtx.clearRect(0, 0, rect.width, rect.height);
      overlayCtx.beginPath();
      overlayCtx.arc((1 - point.x) * rect.width, point.y * rect.height, 8, 0, Math.PI * 2);
      overlayCtx.fillStyle = "#2ee59d";
      overlayCtx.fill();
      overlayCtx.lineWidth = 3;
      overlayCtx.strokeStyle = "#ffffff";
      overlayCtx.stroke();
    }

    function moveGestureCursor(indexTip) {
      const targetX = (1 - indexTip.x) * window.innerWidth;
      const targetY = indexTip.y * window.innerHeight;

      if (smoothX === null || smoothY === null) {
        smoothX = targetX;
        smoothY = targetY;
      } else {
        smoothX = smoothing * targetX + (1 - smoothing) * smoothX;
        smoothY = smoothing * targetY + (1 - smoothing) * smoothY;
      }

      const x = Math.max(0, Math.min(window.innerWidth - 1, smoothX));
      const y = Math.max(0, Math.min(window.innerHeight - 1, smoothY));
      gestureCursor.style.left = `${x}px`;
      gestureCursor.style.top = `${y}px`;
      gestureCursor.classList.add("active");

      const element = document.elementFromPoint(x, y);
      const target = element ? element.closest(".gesture-target, button") : null;
      if (hoveredElement && hoveredElement !== target) {
        hoveredElement.classList.remove("hovered");
      }
      if (target) {
        target.classList.add("hovered");
      }
      hoveredElement = target;
    }

    function dispatchGestureClick() {
      const rect = gestureCursor.getBoundingClientRect();
      const x = rect.left + rect.width / 2;
      const y = rect.top + rect.height / 2;
      const element = document.elementFromPoint(x, y);
      const target = element ? element.closest(".gesture-target, button") : null;

      gestureCursor.classList.add("clicking");
      window.setTimeout(() => gestureCursor.classList.remove("clicking"), 180);

      if (!target || target.disabled || target.id === "activateBtn" || target.id === "stopBtn") {
        setLog("Double blink detected, but no workspace target was under the gesture cursor.");
        lastAction.textContent = "No target selected";
        return;
      }

      target.click();
      target.classList.add("clicked");
      window.setTimeout(() => target.classList.remove("clicked"), 500);
    }

    function processBlink(faceLandmarks) {
      const leftEar = eyeAspectRatio(faceLandmarks, leftEyeIdx);
      const rightEar = eyeAspectRatio(faceLandmarks, rightEyeIdx);
      const avgEar = (leftEar + rightEar) / 2;
      const now = performance.now();

      faceState.textContent = `EAR ${avgEar.toFixed(3)}`;

      if (avgEar < eyeCloseThreshold) {
        closedFrames += 1;
        gestureState.textContent = "Blinking";
        return;
      }

      if (closedFrames >= longBlinkFrames) {
        pendingBlinks = 0;
        gestureState.textContent = "Long blink";
      } else if (closedFrames >= shortBlinkFrames) {
        if (now - lastShortBlink > doubleBlinkWindow) {
          pendingBlinks = 0;
        }

        pendingBlinks += 1;
        lastShortBlink = now;
        gestureState.textContent = pendingBlinks === 1 ? "Blink 1/2" : "Double blink";

        if (pendingBlinks >= 2 && now - lastLeftClick > clickCooldown) {
          lastLeftClick = now;
          pendingBlinks = 0;
          clickCount += 1;
          clickCountEl.textContent = String(clickCount);
          dispatchGestureClick();
        }
      } else if (pendingBlinks > 0 && now - lastShortBlink > doubleBlinkWindow) {
        pendingBlinks = 0;
        gestureState.textContent = "None";
      } else {
        gestureState.textContent = "None";
      }

      closedFrames = 0;
    }

    function loop() {
      if (!running) {
        return;
      }

      if (cameraFeed.currentTime !== lastVideoTime && cameraFeed.videoWidth > 0) {
        lastVideoTime = cameraFeed.currentTime;
        const timestamp = performance.now();
        const handResult = handLandmarker.detectForVideo(cameraFeed, timestamp);
        const faceResult = faceLandmarker.detectForVideo(cameraFeed, timestamp);

        if (handResult.landmarks && handResult.landmarks.length > 0) {
          const indexTip = handResult.landmarks[0][8];
          handState.textContent = "Tracking";
          drawHandPoint(indexTip);
          moveGestureCursor(indexTip);
        } else {
          handState.textContent = "Not found";
          gestureCursor.classList.remove("active");
          const rect = overlay.getBoundingClientRect();
          overlayCtx.clearRect(0, 0, rect.width, rect.height);
        }

        if (faceResult.faceLandmarks && faceResult.faceLandmarks.length > 0) {
          processBlink(faceResult.faceLandmarks[0]);
        } else {
          faceState.textContent = "Not found";
        }
      }

      animationId = requestAnimationFrame(loop);
    }

    async function activateCamera() {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setLog("This browser does not support camera access.");
        return;
      }

      activateBtn.disabled = true;
      setStatus("Starting");

      try {
        await loadModels();
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: "user",
            width: { ideal: 960 },
            height: { ideal: 720 }
          },
          audio: false
        });

        cameraFeed.srcObject = stream;
        await cameraFeed.play();
        resizeOverlay();
        running = true;
        stopBtn.disabled = false;
        setStatus("Live", true);
        setLog("Tracking is active. Move with your index finger and double blink over a workspace target to click.");
        animationId = requestAnimationFrame(loop);
      } catch (error) {
        activateBtn.disabled = false;
        setStatus("Error");
        setLog(`Activation failed: ${error.message}`);
      }
    }

    function stopCamera() {
      running = false;
      if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
      }
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
      }
      cameraFeed.srcObject = null;
      activateBtn.disabled = false;
      stopBtn.disabled = true;
      handState.textContent = "Waiting";
      faceState.textContent = "Waiting";
      gestureState.textContent = "None";
      setStatus("Idle");
      setLog("Tracking stopped.");
      gestureCursor.classList.remove("active");
      overlayCtx.clearRect(0, 0, overlay.width, overlay.height);
    }

    document.querySelectorAll(".gesture-target").forEach((target) => {
      target.addEventListener("click", () => {
        const label = target.dataset.label || "Target";
        lastAction.textContent = `${label} triggered`;
        setLog(`${label} triggered by double blink.`);
      });
    });

    activateBtn.addEventListener("click", activateCamera);
    stopBtn.addEventListener("click", stopCamera);
    window.addEventListener("resize", resizeOverlay);
  </script>
</body>
</html>
"""


def app(environ, start_response):
    body = HTML.encode("utf-8")
    headers = [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ]
    start_response("200 OK", headers)
    return [body]
