# Garbage Detection in Public Zones
import streamlit as st
import cv2
import tempfile
import pandas as pd
import datetime
import numpy as np
from ultralytics import YOLO

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Garbage Detection Tracker", layout="wide")
st.title("🗑️ Garbage Detection in Public Zones")

# ------------------ SIDEBAR ------------------
st.sidebar.header("Upload CCTV Footage")
video_file = st.sidebar.file_uploader("Upload a street surveillance video", type=["mp4", "mov", "avi"])
st.sidebar.markdown("""---""")
st.sidebar.header("Select Cleaning Zone")
selected_zone = st.sidebar.selectbox("Zone", ["Sector 1", "Sector 2", "Sector 3"])

# Simulated cleaning zone data
zone_data = pd.DataFrame({
    "Zone": ["Sector 1", "Sector 2", "Sector 3"],
    "Cleanliness_Rating": [4.2, 2.8, 3.5],
    "Scheduled_Cleaning_Time": ["6 AM", "7 AM", "8 AM"]
})

# Load YOLOv8 model (assumes garbage detection model is available)
model = YOLO("yolov8n.pt")  # Replace with a custom-trained garbage model if available

# ------------------ DETECTION FUNCTION ------------------
def detect_garbage(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    garbage_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 15 != 0:
            continue

        results = model(frame)
        for result in results:
            labels = result.names
            if any(label in ["bottle", "cup", "plastic bag"] for label in labels.values()):
                garbage_count += 1

    cap.release()
    return garbage_count

# ------------------ MAIN PROCESS ------------------
if video_file:
    with tempfile.NamedTemporaryFile(delete=False) as tfile:
        tfile.write(video_file.read())
        garbage_count = detect_garbage(tfile.name)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    log_df = pd.DataFrame({"Time": [timestamp], "Zone": [selected_zone], "Garbage_Detections": [garbage_count]})
    st.success(f"✅ Detected {garbage_count} garbage-like items in uploaded footage.")

    st.subheader("📊 Detection Log")
    st.dataframe(log_df)

    st.subheader("🧹 Zone Cleanliness Info")
    st.dataframe(zone_data[zone_data["Zone"] == selected_zone])

    st.subheader("📤 Feedback to Municipality")
    if garbage_count > 10:
        st.error("🚨 High garbage levels detected. Urgent cleanup needed in this zone.")
    elif garbage_count == 0:
        st.success("✅ No garbage detected. Zone appears clean.")
    else:
        st.warning("⚠️ Some litter found. Consider scheduling extra cleaning.")

else:
    st.info("Upload a street footage video to begin garbage detection analysis.")
