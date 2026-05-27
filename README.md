# Curseflow

Curseflow is a webcam-based hands-free cursor controller:
- Move cursor with your **index finger**.
- **Double blink** performs a left click.
- **Long blink** performs a right click.
- **Auto-calibration** learns your eye threshold in 10 seconds at startup.

## Requirements

- Windows/macOS/Linux with a webcam
- Python 3.10+

## Setup

```powershell
cd C:\Users\Abhishek\Curseflow
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-desktop.txt
```

## Run

```powershell
.\Start-Curseflow.cmd
```

Use `Activate` in the desktop dashboard to start system-wide cursor control. Press `Stop` in the dashboard,
or press `q` or `Esc` in the OpenCV preview window, to exit the camera engine.

You can also run the engine directly:

```powershell
py -3 curseflow.py
```

## Useful tuning flags

```powershell
py -3 curseflow.py --cursor-speed 1.2 --smoothing 0.3
```

- `--cursor-speed`: Pointer sensitivity
- `--smoothing`: Higher value = more responsive, less smooth
- `--eye-close-threshold`: Lower value = harder to trigger blink click
- `--short-blink-frames`: Frames needed for each short blink in the double-blink gesture
- `--long-blink-frames`: Frames for right click
- `--double-blink-window`: Max seconds between the two short blinks
- `--calibration-seconds`: Calibration duration (default: 10)
- `--calibration-ratio`: Open-eye EAR multiplier for threshold (default: 0.72)
- `--no-auto-calibrate`: Skip calibration and use `--eye-close-threshold`

## Notes

- Keep your face and hand in frame for stable tracking.
- On first run, camera permission prompts may appear.
- On first run, hand/face model files are downloaded automatically into `models/`.
- If double-blink clicks are too sensitive, reduce `--double-blink-window`, increase `--short-blink-frames`, and/or lower `--eye-close-threshold`.
- During calibration, keep your eyes naturally open and look at the screen.

## Vercel

This repo now includes an `app.py` Vercel entrypoint that serves a browser dashboard instead of the earlier JSON placeholder.

The dashboard can request webcam access from the user's browser with an `Activate` button, track the index finger with
MediaPipe Tasks Vision, show an on-page gesture cursor, and use double blinks to click workspace targets.

Browser security still prevents a Vercel page from moving the operating system mouse pointer. The deployed app provides
gesture control inside the web page; `curseflow.py` remains the desktop version for OS-level cursor control.
