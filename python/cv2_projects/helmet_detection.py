# 🛵 Helmet Detection for Bike Riders - Webcam Simulation (No Ultralytics)
import streamlit as st
import cv2
import numpy as np
import datetime
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Helmet Detection Demo")
st.title("🛵 Helmet Detection Simulator (Webcam Based - Haar Cascade)")

st.sidebar.header("Monitoring Controls")
selected_zone = st.sidebar.selectbox("Select Zone", ["Accident Zone 1", "Zone 2", "Safe Zone"])
run = st.sidebar.toggle("Start Detection")

# Sample zone risk data
zone_data = pd.DataFrame({
    "Zone": ["Accident Zone 1", "Zone 2", "Safe Zone"],
    "Helmet_Compliance(%)": [42, 67, 89],
    "Accident_Risk": ["High", "Moderate", "Low"]
})

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
helmet_cascade = cv2.CascadeClassifier('helmet_cascade.xml')  # You must train/provide this XML

# Check if helmet cascade is loaded
if helmet_cascade.empty():
    st.warning("⚠️ Helmet cascade not loaded properly. Helmet detection will be skipped (simulated mode).")
    simulate_helmet_detection = True
else:
    simulate_helmet_detection = False

# ---------------- CAMERA DETECTION ----------------
def detect_helmet_webcam():
    cap = cv2.VideoCapture(0)
    FRAME_WINDOW = st.image([])
    log = []

    while run:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        helmets = []
        if not simulate_helmet_detection:
            helmets = helmet_cascade.detectMultiScale(gray, 1.1, 4)

        helmet_count = 0
        head_count = 0

        # Draw helmet boxes
        for (x, y, w, h) in helmets:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Helmet', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            helmet_count += 1

        # Draw face boxes not covered by helmets
        for (x, y, w, h) in faces:
            # Check if this face overlaps with any helmet region
            is_helmet = False
            for (hx, hy, hw, hh) in helmets:
                if abs(x - hx) < w and abs(y - hy) < h:
                    is_helmet = True
                    break
            if not is_helmet:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, 'Head', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                head_count += 1

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        log.append({"Time": datetime.datetime.now(), "Helmet": helmet_count, "Head": head_count})

    cap.release()
    return pd.DataFrame(log)

# ---------------- MAIN ----------------
if run:
    st.info("🔍 Running helmet detection via webcam. Show helmet/cap to camera.")
    result_log = detect_helmet_webcam()

    if not result_log.empty:
        st.subheader("📊 Detection Log (last few)")
        st.dataframe(result_log.tail(5))

        st.subheader("📍 Zone Safety Info")
        st.dataframe(zone_data[zone_data.Zone == selected_zone])

        st.subheader("📢 Helmet Compliance Summary")
        total = result_log.Helmet.sum() + result_log.Head.sum()
        if total == 0:
            st.warning("No detections yet. Show your head/helmet to the webcam.")
        else:
            helmet_pct = result_log.Helmet.sum() / total * 100
            if helmet_pct < 50:
                st.error(f"🚨 Low helmet usage detected ({helmet_pct:.1f}%). High risk zone!")
            elif helmet_pct < 80:
                st.warning(f"⚠️ Moderate helmet usage ({helmet_pct:.1f}%). Issue awareness alerts.")
            else:
                st.success(f"✅ Excellent helmet usage ({helmet_pct:.1f}%). Keep it up!")
else:
    st.info("Turn ON the detection toggle to start webcam analysis.")