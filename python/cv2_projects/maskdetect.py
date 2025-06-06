# 😷 Mask & Social Distancing Monitor (Laptop Webcam Version)
import streamlit as st
import cv2
import tempfile
import numpy as np
from ultralytics import YOLO
import pandas as pd
import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Mask & Social Distancing Monitor")
st.title("😷 Real-Time Mask & Distance Monitor")

st.sidebar.header("Monitoring Options")
selected_zone = st.sidebar.selectbox("Select Zone", ["Zone A", "Zone B", "Zone C"])
run = st.sidebar.toggle("Start Camera")

zone_data = pd.DataFrame({
    "Zone": ["Zone A", "Zone B", "Zone C"],
    "Mask_Compliance": [72, 45, 88],
    "Risk_Level": ["Moderate", "High", "Low"]
})

# Load YOLOv8 model with mask + face detection capability (custom model recommended)
model = YOLO("yolov8n.pt")  # Replace with trained mask detection model

# ---------------- CAMERA DETECTION ----------------
def detect_and_display():
    cap = cv2.VideoCapture(0)
    FRAME_WINDOW = st.image([])
    log = []

    while run:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        people = []
        masks = 0

        for r in results:
            for box, cls in zip(r.boxes.xyxy, r.boxes.cls):
                label = r.names[int(cls)]
                x1, y1, x2, y2 = map(int, box[:4])

                if label in ["person", "face", "mask"]:
                    people.append((x1, y1, x2, y2))
                    if label == "mask":
                        masks += 1

                color = (0, 255, 0) if label == "mask" else (255, 0, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Estimate distances (simplified)
        for i in range(len(people)):
            for j in range(i + 1, len(people)):
                xi, yi, _, _ = people[i]
                xj, yj, _, _ = people[j]
                dist = np.linalg.norm(np.array([xi, yi]) - np.array([xj, yj]))
                if dist < 100:
                    cv2.line(frame, (xi, yi), (xj, yj), (0, 0, 255), 2)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        log.append({"time": datetime.datetime.now(), "masks": masks, "people": len(people)})

    cap.release()
    return pd.DataFrame(log)

# ---------------- MAIN ----------------
if run:
    st.info("📸 Running webcam... Allow permissions.")
    result_log = detect_and_display()
    if not result_log.empty:
        st.subheader("📊 Session Summary")
        st.dataframe(result_log.tail(5))

        st.subheader("📍 Zone Info")
        st.dataframe(zone_data[zone_data.Zone == selected_zone])

        st.subheader("💡 Recommendations")
        avg_mask_rate = result_log["masks"].sum() / max(result_log["people"].sum(), 1) * 100
        if avg_mask_rate < 50:
            st.error("🚨 Low mask usage detected. Consider mask enforcement in this zone.")
        elif avg_mask_rate < 80:
            st.warning("⚠️ Moderate compliance. Issue awareness alerts.")
        else:
            st.success("✅ Good compliance. Maintain current protocols.")
else:
    st.info("Toggle 'Start Camera' to begin real-time monitoring with webcam.")