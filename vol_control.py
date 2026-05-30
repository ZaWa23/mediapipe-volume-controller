import cv2
import mediapipe as mp
import numpy as np
from math import hypot

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

devices = AudioUtilities.GetSpeakers()

interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))

min_vol, max_vol, _ = volume.GetVolumeRange()


# =========================
# MEDIAPIPE SETUP
# =========================
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

model_path = "hand_landmarker.task"

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

cap = cv2.VideoCapture(0, cv2.CAP_ANY)

THUMB_TIP = 4
INDEX_TIP = 8


# =========================
# MAIN LOOP
# =========================

prev_length = 0
alpha = 0.2   # lower = smoother, higher = more responsive
prev_vol = min_vol
vol_alpha = 0.25

with HandLandmarker.create_from_options(options) as landmarker:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        result = landmarker.detect_for_video(mp_image, timestamp)

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            thumb = hand[THUMB_TIP]
            index = hand[INDEX_TIP]

            x1, y1 = int(thumb.x * w), int(thumb.y * h)
            x2, y2 = int(index.x * w), int(index.y * h)

            # draw points
            cv2.circle(frame, (x1, y1), 10, (255, 0, 0), -1)
            cv2.circle(frame, (x2, y2), 10, (255, 0, 0), -1)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # distance between fingers

            raw_length = hypot(x2 - x1, y2 - y1)

            length = prev_length * (1 - alpha) + raw_length * alpha
            prev_length = length




            # =========================
            # REAL SYSTEM VOLUME CONTROL
            # =========================
            vol = np.interp(length, [20, 200], [min_vol, max_vol])
            vol = np.clip(vol, min_vol, max_vol)

            prev_vol = prev_vol * (1 - vol_alpha) + vol * vol_alpha
            volume.SetMasterVolumeLevel(prev_vol, None)
            # =========================
            # VISUAL BAR (JUST DISPLAY)
            # =========================
            vol_bar = np.interp(length, [20, 200], [400, 150])

            cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), -1)

            cv2.putText(frame, "REAL Volume Control", (50, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (255, 255, 255), 2)

        cv2.imshow("Hand Volume Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()