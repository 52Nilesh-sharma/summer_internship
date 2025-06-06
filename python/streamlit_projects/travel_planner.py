import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu

# ---------- CONFIG ----------
ORS_API_KEY = "5b3ce3597851110001cf62486752537ac5844013b2c41c34c90da271"

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Travel Planner", layout="wide")

# ---------- SIDEBAR MENU ----------
with st.sidebar:
    selected = option_menu(
        "Travel Menu",
        ["Plan Route", "Nearby Attractions", "Transport Options"],
        icons=["geo", "map", "bus"],
        menu_icon="compass",
        default_index=0,
    )

# ---------- FUNCTIONS ----------
def get_coordinates(place):
    url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200 and response.content:
        try:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
        except Exception as e:
            st.error(f"Error parsing location data: {e}")

    return None

def get_route(src, dst):
    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    route_data = {
        "coordinates": [
            [src[1], src[0]],
            [dst[1], dst[0]]
        ],
        "format": "geojson"
    }
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    response = requests.post(url, headers=headers, json=route_data)
    return response.json() if response.status_code == 200 else None

def get_wikipedia_places(place):
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={place}&limit=5&namespace=0&format=json"
    res = requests.get(url).json()
    return list(zip(res[1], res[2], res[3]))

def estimate_transport_fare(mode, distance_km):
    fares = {
        "auto": 15,   # ₹ per km
        "metro": 5,
        "bus": 1.5,
        "train": 1.2
    }
    return round(distance_km * fares.get(mode, 2))

# ---------- MAIN ----------
if selected == "Plan Route":
    st.title("🚗 Smart Travel Planner")
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Enter Source", "Delhi")
    with col2:
        destination = st.text_input("Enter Destination", "Manali")

    if st.button("🚀 Plan My Route"):
        src_coords = get_coordinates(source)
        dst_coords = get_coordinates(destination)

        if not src_coords or not dst_coords:
            st.error("Could not locate one of the locations.")
        else:
            route = get_route(src_coords, dst_coords)
            if route:
                props = route['features'][0]['properties']['summary']
                distance = round(props['distance'] / 1000, 2)
                duration = round(props['duration'] / 3600, 2)

                st.success(f"🛣 {distance} km | ⏱ {duration} hrs")

                df_map = pd.DataFrame({
                    "latitude": [src_coords[0], dst_coords[0]],
                    "longitude": [src_coords[1], dst_coords[1]]
                })
                st.map(df_map)
            else:
                st.error("Couldn't fetch route.")

elif selected == "Nearby Attractions":
    st.title("🗺 Explore Nearby Attractions")
    place = st.text_input("Enter a Place to Explore", "Manali")
    if st.button("🔍 Show Attractions"):
        attractions = get_wikipedia_places(place)
        for title, desc, link in attractions:
            st.markdown(f"### [{title}]({link})\n{desc}")

elif selected == "Transport Options":
    st.title("🚌 Transport Mode Comparison")
    source = st.text_input("Source City", "Delhi", key="src_trans")
    destination = st.text_input("Destination City", "Manali", key="dst_trans")

    if st.button("Compare Modes"):
        src_coords = get_coordinates(source)
        dst_coords = get_coordinates(destination)

        if not src_coords or not dst_coords:
            st.error("Location not found.")
        else:
            route = get_route(src_coords, dst_coords)
            if route:
                distance_km = round(route['features'][0]['properties']['summary']['distance'] / 1000, 2)
                st.success(f"🛣 Total Distance: {distance_km} km")

                st.subheader("🚖 Auto / Metro")
                st.info(f"Estimated Fare: ₹{estimate_transport_fare('auto', distance_km)}")

                st.subheader("🚌 Bus")
                st.info(f"Estimated Fare: ₹{estimate_transport_fare('bus', distance_km)}")

                st.subheader("🚆 Train")
                st.info(f"Estimated Fare: ₹{estimate_transport_fare('train', distance_km)}")

                st.warning("Note: Actual fares may vary. These are estimated averages.")
            else:
                st.error("Unable to fetch transport data.")