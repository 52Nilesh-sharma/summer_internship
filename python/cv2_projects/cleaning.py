# ✋ Hand Gesture-Based Cleaner Request System (OpenCV + Mediapipe)
import streamlit as st
import cv2
import datetime
import pandas as pd
import numpy as np

try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    use_mediapipe = True
except ImportError:
    mp_hands = None
    mp_drawing = None
    use_mediapipe = False

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Cleaner Request via Hand Gesture")
st.title("✋ Cleaner Request Trigger (Raise Hand to Signal)")

st.sidebar.header("Zone Settings")
selected_zone = st.sidebar.selectbox("Select Zone", ["Zone A", "Zone B", "Dirty Spot 1", "Public Washroom"])
run = st.sidebar.toggle("Start Camera")

# ---------------- HELPERS ----------------
request_log = []

# Detect hand using Mediapipe (more accurate)
def detect_hand_mediapipe(frame, hands):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        return True
    return False

# Detect hand using OpenCV (skin color + contour)
def detect_hand_opencv(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 3000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return True
    return False

# ---------------- MAIN DETECTION ----------------
def run_camera():
    cap = cv2.VideoCapture(0)
    FRAME_WINDOW = st.image([])
    detected = False
    log = []

    if use_mediapipe:
        with mp_hands.Hands(max_num_hands=1) as hands:
            while run:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                hand_found = detect_hand_mediapipe(frame, hands)

                if hand_found and not detected:
                    timestamp = datetime.datetime.now()
                    log.append({"Time": timestamp, "Zone": selected_zone})
                    st.success(f"🧹 Cleaner Request Sent for {selected_zone} at {timestamp.strftime('%H:%M:%S')}")
                    detected = True

                elif not hand_found:
                    detected = False

                FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    else:
        while run:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            hand_found = detect_hand_opencv(frame)

            if hand_found and not detected:
                timestamp = datetime.datetime.now()
                log.append({"Time": timestamp, "Zone": selected_zone})
                st.success(f"🧹 Cleaner Request Sent for {selected_zone} at {timestamp.strftime('%H:%M:%S')}")
                detected = True

            elif not hand_found:
                detected = False

            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()
    return pd.DataFrame(log)

# ---------------- RUN ----------------
if run:
    if use_mediapipe:
        st.info("✅ Mediapipe detected. Using accurate hand tracking.")
    else:
        st.warning("⚠️ Mediapipe not installed. Using basic OpenCV hand detection.")

    st.info("Raise your hand (✋) to request cleaning.")
    log_df = run_camera()

    if not log_df.empty:
        st.subheader("📝 Cleaner Request Log")
        st.dataframe(log_df)
else:
    st.info("Toggle 'Start Camera' to begin hand gesture detection.")