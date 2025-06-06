import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu

# --------- CONFIG ---------
ORS_API_KEY = "5b3ce3597851110001cf62486752537ac5844013b2c41c34c90da271"

st.set_page_config(page_title="CityPulse", layout="wide")

st.markdown("""
    <style>
    body { background-color: #f8f5ff; }
    .stApp { background-color: #f8f5ff; }
    .css-18e3th9 { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# --------- STATE ---------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --------- LOGIN ---------
if not st.session_state.logged_in:
    st.title("🚦 CityPulse – Local Travel & Cost Optimizer")
    username = st.text_input("Enter your username to start")
    if username:
        st.session_state.username = username
        st.session_state.logged_in = True
        st.success(f"Welcome {username}! Use sidebar to navigate.")
    st.stop()

# --------- SIDEBAR MENU ---------
with st.sidebar:
    selected = option_menu("Navigate", ["Dashboard", "Nearby Attractions"], 
        icons=["geo-alt", "binoculars"], menu_icon="compass", default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#ede9fe"},
            "icon": {"color": "#6a0dad", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#c4b5fd"},
        })

# --------- FUNCTIONS ---------
def get_coordinates(place):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={place}"
    res = requests.get(url).json()
    if res:
        return float(res[0]["lat"]), float(res[0]["lon"])
    return None

def get_route(src, dest):
    coords = [[src[1], src[0]], [dest[1], dest[0]]]
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
    res = requests.post(url, headers=headers, json={"coordinates": coords}).json()
    dist = res["features"][0]["properties"]["segments"][0]["distance"] / 1000
    dur = res["features"][0]["properties"]["segments"][0]["duration"] / 60
    geo = res["features"][0]["geometry"]
    return round(dist, 2), round(dur, 2), geo

def estimate_fares(km):
    return {
        "Auto": round(30 + 15 * km),
        "Metro": round(10 + 5 * km),
        "Bus": round(5 + 2 * km),
        "Train": round(20 + 10 * km)
    }

def get_nearby(lat, lon):
    query = f"""
    [out:json];
    (
      node["tourism"](around:1000,{lat},{lon});
      node["amenity"](around:1000,{lat},{lon});
    );
    out center;
    """
    res = requests.post("http://overpass-api.de/api/interpreter", data=query)
    elements = res.json()["elements"]
    return [{
        "name": el["tags"].get("name", "Unnamed"),
        "type": el["tags"].get("tourism", el["tags"].get("amenity", "POI")),
        "lat": el["lat"],
        "lon": el["lon"]
    } for el in elements]

# --------- DASHBOARD ---------
if selected == "Dashboard":
    st.header("🧭 Route & Fare Planner")

    col1, col2 = st.columns(2)
    with col1:
        src_place = st.text_input("Enter source")
    with col2:
        dest_place = st.text_input("Enter destination")

    if src_place and dest_place:
        src = get_coordinates(src_place)
        dest = get_coordinates(dest_place)

        if src and dest:
            km, mins, geo = get_route(src, dest)
            st.success(f"Distance: {km} km | Duration: {mins} mins")

            fares = estimate_fares(km)
            df = pd.DataFrame(fares.items(), columns=["Mode", "Fare (₹)"]).sort_values("Fare (₹)")
            st.subheader("💸 Estimated Fare Comparison")
            st.dataframe(df, use_container_width=True)

            st.subheader("🗺️ Route Map")
            fmap = folium.Map(location=src, zoom_start=13)
            folium.Marker(src, tooltip="Source", icon=folium.Icon(color="green")).add_to(fmap)
            folium.Marker(dest, tooltip="Destination", icon=folium.Icon(color="red")).add_to(fmap)
            folium.PolyLine([(lat, lon) for lon, lat in geo["coordinates"]], color="purple", weight=4).add_to(fmap)
            st_folium(fmap, width=700, height=500)
        else:
            st.error("❌ Invalid source or destination entered.")

# --------- NEARBY ATTRACTIONS ---------
elif selected == "Nearby Attractions":
    st.header("📍 Discover Places Around You")

    place = st.text_input("Enter location")
    if place:
        coords = get_coordinates(place)
        if coords:
            st.success(f"Showing results near {place}")
            pois = get_nearby(*coords)
            if pois:
                df = pd.DataFrame(pois)
                st.dataframe(df)
                m = folium.Map(location=coords, zoom_start=14)
                for p in pois:
                    folium.Marker([p["lat"], p["lon"]],
                                  tooltip=f"{p['name']} ({p['type']})",
                                  icon=folium.Icon(color="blue")).add_to(m)
                st_folium(m, width=700, height=500)
            else:
                st.warning("No nearby places found.")
        else:
            st.error("❌ Location not found.")
