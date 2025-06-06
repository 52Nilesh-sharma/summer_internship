# Smart Footpath Usage Tracker
import streamlit as st
import cv2
import tempfile
import pandas as pd
import plotly.express as px
import datetime
import os

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Smart Footpath Usage Tracker", layout="wide")
st.title("🚶 Smart Footpath Usage Tracker")

# ------------------ SIDEBAR ------------------
st.sidebar.header("Upload CCTV Footage")
video_file = st.sidebar.file_uploader("Upload a footpath video", type=["mp4", "mov", "avi"])
st.sidebar.markdown("""---""")
st.sidebar.header("Select Zone")
selected_zone = st.sidebar.selectbox("Zone", ["MG Road", "JP Nagar", "Indiranagar"])

# Simulated zone data
zone_data = pd.DataFrame({
    "Zone": ["MG Road", "JP Nagar", "Indiranagar"],
    "Width_m": [1.2, 0.8, 1.5],
    "Accessibility": ["Wheelchair", "No Ramp", "Wheelchair"],
    "Condition": ["Good", "Poor", "Average"]
})

# ------------------ DETECTION MODEL ------------------
def detect_pedestrians(video_path):
    cap = cv2.VideoCapture(video_path)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    frame_count = 0
    total_pedestrians = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 10 != 0:
            continue

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        boxes, _ = hog.detectMultiScale(gray, winStride=(8, 8))
        total_pedestrians += len(boxes)

    cap.release()
    return total_pedestrians

# ------------------ PROCESS VIDEO ------------------
if video_file:
    with tempfile.NamedTemporaryFile(delete=False) as tfile:
        tfile.write(video_file.read())
        pedestrian_count = detect_pedestrians(tfile.name)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    log_df = pd.DataFrame({"Time": [timestamp], "Zone": [selected_zone], "Count": [pedestrian_count]})
    st.success(f"✅ Detected {pedestrian_count} pedestrians in the uploaded footage.")

    # Show chart
    st.subheader("📊 Footpath Usage Log")
    st.dataframe(log_df)

    st.subheader("📍 Zone Info")
    st.dataframe(zone_data[zone_data["Zone"] == selected_zone])

    # Urban recommendation logic
    st.subheader("💡 Urban Design Recommendation")
    zone_info = zone_data[zone_data["Zone"] == selected_zone].iloc[0]
    if pedestrian_count > 50:
        st.warning(f"🚧 High foot traffic detected. Consider widening the footpath at {selected_zone}.")
    elif pedestrian_count == 0:
        st.info(f"ℹ️ No foot traffic detected. Consider repurposing space or increasing accessibility.")
    else:
        st.success(f"✅ Footpath usage normal. Maintain current infrastructure.")

else:
    st.info("Upload a video file from a footpath zone to begin analysis.")
