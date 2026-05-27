HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Curseflow Dashboard</title>
  <style>
    :root {
      --bg: #f5efe4;
      --panel: rgba(255, 252, 246, 0.82);
      --ink: #1c1917;
      --muted: #6b645d;
      --accent: #c2551a;
      --accent-dark: #8f3d14;
      --line: rgba(28, 25, 23, 0.12);
      --success: #1f7a4d;
      --shadow: 0 24px 60px rgba(88, 61, 32, 0.18);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(194, 85, 26, 0.18), transparent 30%),
        radial-gradient(circle at bottom right, rgba(31, 122, 77, 0.16), transparent 24%),
        linear-gradient(135deg, #f8f3ea, #efe4d2 58%, #e5d6bf);
    }

    .shell {
      width: min(1120px, calc(100vw - 32px));
      margin: 24px auto;
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 28px;
      background: var(--panel);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }

    .hero {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 24px;
      align-items: stretch;
    }

    .eyebrow {
      display: inline-block;
      padding: 8px 12px;
      border-radius: 999px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-size: 12px;
      background: rgba(194, 85, 26, 0.1);
      color: var(--accent-dark);
    }

    h1 {
      margin: 16px 0 12px;
      font-size: clamp(40px, 7vw, 72px);
      line-height: 0.92;
      letter-spacing: -0.04em;
    }

    .lead {
      margin: 0 0 22px;
      max-width: 48ch;
      font-size: 18px;
      line-height: 1.6;
      color: var(--muted);
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 18px;
    }

    button {
      appearance: none;
      border: 0;
      border-radius: 999px;
      padding: 14px 22px;
      font: inherit;
      font-size: 16px;
      cursor: pointer;
      transition: transform 160ms ease, opacity 160ms ease, background 160ms ease;
    }

    button:hover {
      transform: translateY(-1px);
    }

    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    .primary {
      background: var(--accent);
      color: #fff8f3;
    }

    .secondary {
      background: rgba(28, 25, 23, 0.08);
      color: var(--ink);
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 18px;
    }

    .card {
      padding: 16px;
      border-radius: 20px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.55);
    }

    .card h2,
    .panel h2 {
      margin: 0 0 8px;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
    }

    .card strong {
      display: block;
      font-size: 22px;
      line-height: 1.2;
    }

    .panel {
      position: relative;
      overflow: hidden;
      min-height: 420px;
      border-radius: 24px;
      border: 1px solid var(--line);
      background:
        linear-gradient(180deg, rgba(28, 25, 23, 0.06), rgba(28, 25, 23, 0.18)),
        linear-gradient(145deg, #2c241f, #5c4435);
      padding: 18px;
      color: #f8f3ea;
    }

    .statusbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 13px;
      background: rgba(255, 255, 255, 0.12);
    }

    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #f5b942;
      box-shadow: 0 0 0 6px rgba(245, 185, 66, 0.18);
      transition: background 160ms ease, box-shadow 160ms ease;
    }

    .dot.live {
      background: #5de2a5;
      box-shadow: 0 0 0 6px rgba(93, 226, 165, 0.18);
    }

    .viewport {
      position: relative;
      height: 320px;
      border-radius: 18px;
      overflow: hidden;
      background:
        radial-gradient(circle at center, rgba(194, 85, 26, 0.35), transparent 42%),
        linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(0, 0, 0, 0.28));
      border: 1px solid rgba(255, 255, 255, 0.14);
    }

    video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: none;
      transform: scaleX(-1);
      background: #000;
    }

    .placeholder {
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      padding: 24px;
      text-align: center;
    }

    .placeholder strong {
      display: block;
      margin-bottom: 10px;
      font-size: 28px;
      letter-spacing: -0.04em;
    }

    .placeholder p {
      margin: 0 auto;
      max-width: 28ch;
      color: rgba(248, 243, 234, 0.8);
      line-height: 1.5;
    }

    .note {
      margin-top: 14px;
      font-size: 14px;
      line-height: 1.6;
      color: rgba(248, 243, 234, 0.82);
    }

    .log {
      margin-top: 16px;
      padding: 14px 16px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.08);
      font-size: 14px;
      line-height: 1.5;
      min-height: 76px;
    }

    .footer {
      margin-top: 24px;
      padding-top: 18px;
      border-top: 1px solid var(--line);
      font-size: 14px;
      line-height: 1.6;
      color: var(--muted);
    }

    @media (max-width: 900px) {
      .hero {
        grid-template-columns: 1fr;
      }

      .grid {
        grid-template-columns: 1fr;
      }

      .shell {
        padding: 20px;
      }
    }
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div>
        <span class="eyebrow">Browser Dashboard</span>
        <h1>Curseflow</h1>
        <p class="lead">
          Activate your webcam from the browser and preview the camera feed inside a deployed Vercel dashboard.
          This web version can access the browser camera after permission is granted.
        </p>
        <div class="actions">
          <button id="activateBtn" class="primary" type="button">Activate Camera</button>
          <button id="stopBtn" class="secondary" type="button" disabled>Stop Camera</button>
        </div>
        <div class="grid">
          <article class="card">
            <h2>Status</h2>
            <strong id="cameraState">Idle</strong>
          </article>
          <article class="card">
            <h2>Permission</h2>
            <strong id="permissionState">Not Requested</strong>
          </article>
          <article class="card">
            <h2>Platform</h2>
            <strong>Vercel + Browser Camera</strong>
          </article>
        </div>
      </div>
      <section class="panel">
        <div class="statusbar">
          <h2>Live Preview</h2>
          <div class="badge"><span id="liveDot" class="dot"></span><span id="liveLabel">Awaiting activation</span></div>
        </div>
        <div class="viewport">
          <video id="cameraFeed" autoplay playsinline muted></video>
          <div id="placeholder" class="placeholder">
            <div>
              <strong>Webcam standby</strong>
              <p>Click <em>Activate Camera</em>, approve browser permissions, and the live preview will appear here.</p>
            </div>
          </div>
        </div>
        <div class="log" id="eventLog">Waiting for camera activation.</div>
        <p class="note">
          Browser access is possible on Vercel. Direct desktop cursor control from `curseflow.py` is still a separate local app.
        </p>
      </section>
    </section>
    <section class="footer">
      This deployment now serves a real dashboard instead of the previous JSON placeholder response.
    </section>
  </main>
  <script>
    const activateBtn = document.getElementById("activateBtn");
    const stopBtn = document.getElementById("stopBtn");
    const cameraFeed = document.getElementById("cameraFeed");
    const placeholder = document.getElementById("placeholder");
    const cameraState = document.getElementById("cameraState");
    const permissionState = document.getElementById("permissionState");
    const liveDot = document.getElementById("liveDot");
    const liveLabel = document.getElementById("liveLabel");
    const eventLog = document.getElementById("eventLog");

    let stream = null;

    function setLog(message) {
      eventLog.textContent = message;
    }

    function setIdleState() {
      cameraState.textContent = "Idle";
      liveLabel.textContent = "Awaiting activation";
      liveDot.classList.remove("live");
      activateBtn.disabled = false;
      stopBtn.disabled = true;
      cameraFeed.style.display = "none";
      placeholder.style.display = "grid";
    }

    async function activateCamera() {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        permissionState.textContent = "Unsupported";
        setLog("This browser does not support webcam access through getUserMedia.");
        return;
      }

      activateBtn.disabled = true;
      setLog("Requesting camera permission from the browser...");
      cameraState.textContent = "Requesting Access";

      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user" },
          audio: false
        });

        cameraFeed.srcObject = stream;
        cameraFeed.style.display = "block";
        placeholder.style.display = "none";
        stopBtn.disabled = false;
        permissionState.textContent = "Granted";
        cameraState.textContent = "Live";
        liveLabel.textContent = "Camera active";
        liveDot.classList.add("live");
        setLog("Camera activated successfully. Live preview is now running in the browser.");
      } catch (error) {
        permissionState.textContent = "Denied or Failed";
        cameraState.textContent = "Blocked";
        activateBtn.disabled = false;
        setLog("Camera activation failed: " + error.message);
      }
    }

    function stopCamera() {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
      }

      cameraFeed.srcObject = null;
      permissionState.textContent = "Stopped";
      setLog("Camera stopped.");
      setIdleState();
    }

    activateBtn.addEventListener("click", activateCamera);
    stopBtn.addEventListener("click", stopCamera);
    setIdleState();
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
