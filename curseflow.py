import argparse
import math
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp
import pyautogui
from mediapipe.tasks import python as mp_python_tasks
from mediapipe.tasks.python import vision as mp_vision_tasks


pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


@dataclass
class EyeState:
    closed_frames: int = 0
    pending_left_blinks: int = 0
    last_short_blink: float = 0.0
    last_left_click: float = 0.0
    last_right_click: float = 0.0


class CursorSmoother:
    def __init__(self, alpha: float = 0.25):
        self.alpha = alpha
        self.prev_x = None
        self.prev_y = None

    def smooth(self, x: float, y: float) -> tuple[float, float]:
        if self.prev_x is None or self.prev_y is None:
            self.prev_x, self.prev_y = x, y
            return x, y
        sx = self.alpha * x + (1.0 - self.alpha) * self.prev_x
        sy = self.alpha * y + (1.0 - self.alpha) * self.prev_y
        self.prev_x, self.prev_y = sx, sy
        return sx, sy


def dist(a, b) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def eye_aspect_ratio(landmarks, idx) -> float:
    p1 = landmarks[idx[0]]
    p2 = landmarks[idx[1]]
    p3 = landmarks[idx[2]]
    p4 = landmarks[idx[3]]
    p5 = landmarks[idx[4]]
    p6 = landmarks[idx[5]]
    vertical = dist(p2, p6) + dist(p3, p5)
    horizontal = 2.0 * dist(p1, p4)
    if horizontal == 0:
        return 0.0
    return vertical / horizontal


def move_cursor_from_index_finger(
    frame_w: int,
    frame_h: int,
    index_tip,
    smoother: CursorSmoother,
    speed: float,
) -> tuple[int, int]:
    screen_w, screen_h = pyautogui.size()
    raw_x = (index_tip.x * screen_w) * speed
    raw_y = (index_tip.y * screen_h) * speed
    raw_x = max(0, min(screen_w - 1, raw_x))
    raw_y = max(0, min(screen_h - 1, raw_y))
    sx, sy = smoother.smooth(raw_x, raw_y)
    pyautogui.moveTo(int(sx), int(sy))
    fx = int(index_tip.x * frame_w)
    fy = int(index_tip.y * frame_h)
    return fx, fy


def ensure_model(model_dir: Path, file_name: str, url: str) -> Path:
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / file_name
    if not model_path.exists():
        urllib.request.urlretrieve(url, model_path)
    return model_path


def calibrate_eye_threshold(cap, face_landmarker, left_eye_idx, right_eye_idx, seconds: float, ratio: float):
    samples = []
    start = time.time()
    frame_ts = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        frame_h, _ = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        face_results = face_landmarker.detect_for_video(mp_image, frame_ts)
        frame_ts += 33

        if face_results.face_landmarks:
            face_lm = face_results.face_landmarks[0]
            left_ear = eye_aspect_ratio(face_lm, left_eye_idx)
            right_ear = eye_aspect_ratio(face_lm, right_eye_idx)
            avg_ear = (left_ear + right_ear) / 2.0
            samples.append(avg_ear)
            cv2.putText(
                frame,
                f"Calibrating EAR: {avg_ear:.3f}",
                (12, 32),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 255, 255),
                2,
            )
        else:
            cv2.putText(
                frame,
                "Face not detected. Keep face centered.",
                (12, 32),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 165, 255),
                2,
            )

        remaining = max(0.0, seconds - (time.time() - start))
        cv2.putText(
            frame,
            f"Keep eyes open | Calibration ends in {remaining:.1f}s",
            (12, frame_h - 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
        cv2.imshow("Curseflow", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord("q"):
            return None
        if time.time() - start >= seconds:
            break

    if len(samples) < 20:
        return None
    baseline = sum(samples) / len(samples)
    return baseline * ratio


def run(args):
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError("Unable to open webcam. Check camera index and permissions.")

    model_dir = Path(args.model_dir)
    hand_model_path = ensure_model(
        model_dir,
        "hand_landmarker.task",
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
    )
    face_model_path = ensure_model(
        model_dir,
        "face_landmarker.task",
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
    )

    base_hand_options = mp_python_tasks.BaseOptions(model_asset_path=str(hand_model_path))
    hand_options = mp_vision_tasks.HandLandmarkerOptions(
        base_options=base_hand_options,
        running_mode=mp_vision_tasks.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.6,
    )
    base_face_options = mp_python_tasks.BaseOptions(model_asset_path=str(face_model_path))
    face_options = mp_vision_tasks.FaceLandmarkerOptions(
        base_options=base_face_options,
        running_mode=mp_vision_tasks.RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.6,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    smoother = CursorSmoother(alpha=args.smoothing)
    eye_state = EyeState()

    left_eye_idx = [33, 160, 158, 133, 153, 144]
    right_eye_idx = [362, 385, 387, 263, 373, 380]

    with mp_vision_tasks.HandLandmarker.create_from_options(hand_options) as hands, mp_vision_tasks.FaceLandmarker.create_from_options(face_options) as face_mesh:
        eye_threshold = args.eye_close_threshold
        if args.auto_calibrate:
            calibrated = calibrate_eye_threshold(
                cap,
                face_mesh,
                left_eye_idx,
                right_eye_idx,
                seconds=args.calibration_seconds,
                ratio=args.calibration_ratio,
            )
            if calibrated is not None:
                eye_threshold = calibrated

        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            frame_h, frame_w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            frame_ts = int(time.time() * 1000)

            hand_results = hands.detect_for_video(mp_image, frame_ts)
            face_results = face_mesh.detect_for_video(mp_image, frame_ts)

            if hand_results.hand_landmarks:
                hand_lm = hand_results.hand_landmarks[0]
                idx_tip = hand_lm[8]
                ix, iy = move_cursor_from_index_finger(
                    frame_w, frame_h, idx_tip, smoother, args.cursor_speed
                )
                cv2.circle(frame, (ix, iy), 8, (0, 255, 0), -1)
                for lm in hand_lm:
                    hx, hy = int(lm.x * frame_w), int(lm.y * frame_h)
                    cv2.circle(frame, (hx, hy), 2, (255, 200, 0), -1)

            if face_results.face_landmarks:
                face_lm = face_results.face_landmarks[0]
                left_ear = eye_aspect_ratio(face_lm, left_eye_idx)
                right_ear = eye_aspect_ratio(face_lm, right_eye_idx)
                avg_ear = (left_ear + right_ear) / 2.0
                now = time.time()

                if avg_ear < eye_threshold:
                    eye_state.closed_frames += 1
                else:
                    if eye_state.closed_frames >= args.long_blink_frames:
                        eye_state.pending_left_blinks = 0
                        if now - eye_state.last_right_click > args.click_cooldown:
                            pyautogui.rightClick()
                            eye_state.last_right_click = now
                    elif eye_state.closed_frames >= args.short_blink_frames:
                        if now - eye_state.last_short_blink > args.double_blink_window:
                            eye_state.pending_left_blinks = 0
                        eye_state.pending_left_blinks += 1
                        eye_state.last_short_blink = now
                        if (
                            eye_state.pending_left_blinks >= 2
                            and now - eye_state.last_left_click > args.click_cooldown
                        ):
                            pyautogui.click()
                            eye_state.last_left_click = now
                            eye_state.pending_left_blinks = 0
                    eye_state.closed_frames = 0

                if (
                    eye_state.pending_left_blinks > 0
                    and now - eye_state.last_short_blink > args.double_blink_window
                ):
                    eye_state.pending_left_blinks = 0

                cv2.putText(
                    frame,
                    f"EAR: {avg_ear:.3f}",
                    (12, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    f"Threshold: {eye_threshold:.3f}",
                    (12, 58),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 255),
                    2,
                )

            cv2.putText(
                frame,
                "Curseflow | Finger=Move | Double Blink=Left Click | Long Blink=Right Click",
                (12, frame_h - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1,
            )

            cv2.imshow("Curseflow", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Curseflow: Webcam cursor and click control with finger + eye gestures."
    )
    parser.add_argument("--camera", type=int, default=0, help="Webcam index.")
    parser.add_argument(
        "--smoothing",
        type=float,
        default=0.28,
        help="Cursor smoothing factor between 0 and 1.",
    )
    parser.add_argument(
        "--cursor-speed",
        type=float,
        default=1.0,
        help="Cursor speed multiplier.",
    )
    parser.add_argument(
        "--eye-close-threshold",
        type=float,
        default=0.21,
        help="Lower means stricter blink detection.",
    )
    parser.add_argument(
        "--short-blink-frames",
        type=int,
        default=2,
        help="Closed-eye frames to trigger left click.",
    )
    parser.add_argument(
        "--long-blink-frames",
        type=int,
        default=5,
        help="Closed-eye frames to trigger right click.",
    )
    parser.add_argument(
        "--click-cooldown",
        type=float,
        default=0.45,
        help="Seconds between click actions.",
    )
    parser.add_argument(
        "--double-blink-window",
        type=float,
        default=0.7,
        help="Seconds allowed between two short blinks for a left click.",
    )
    parser.add_argument(
        "--auto-calibrate",
        action="store_true",
        default=True,
        help="Run startup eye-threshold calibration.",
    )
    parser.add_argument(
        "--no-auto-calibrate",
        dest="auto_calibrate",
        action="store_false",
        help="Disable startup calibration and use --eye-close-threshold directly.",
    )
    parser.add_argument(
        "--calibration-seconds",
        type=float,
        default=10.0,
        help="Duration of startup eye calibration.",
    )
    parser.add_argument(
        "--calibration-ratio",
        type=float,
        default=0.72,
        help="Threshold ratio applied to open-eye EAR baseline.",
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default=str(Path(__file__).resolve().parent / "models"),
        help="Directory where mediapipe .task model files are stored.",
    )
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    run(args)
