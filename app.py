import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import distance as geopy_distance
import pydeck as pdk

st.set_page_config(page_title="EV Charging Station Locator", layout="centered")
st.title("🔋 EV Charging Station Locator with Map & Route")
st.markdown("Enter any Hyderabad area or landmark:")

ev_stations = [
    {"name": "EV Fast Charge - Hitech", "lat": 17.4502, "lon": 78.3826},
    {"name": "EV Point - Gachibowli", "lat": 17.4445, "lon": 78.3816},
    {"name": "EV Hub - Banjara Hills", "lat": 17.4095, "lon": 78.4421},
    {"name": "EV Plug - Jubilee Hills", "lat": 17.4275, "lon": 78.4081},
    {"name": "Green EV - Dilsukhnagar", "lat": 17.3705, "lon": 78.5181},
    {"name": "Ultra EV - Ameerpet", "lat": 17.4375, "lon": 78.4483},
    {"name": "FastCharge - Madhapur", "lat": 17.4412, "lon": 78.3912},
    {"name": "EcoEV - LB Nagar", "lat": 17.3522, "lon": 78.5524},
    {"name": "Rapid EV - Mehdipatnam", "lat": 17.3931, "lon": 78.4375},
    {"name": "VoltZone - Kukatpally", "lat": 17.4948, "lon": 78.3994},
]

geolocator = Nominatim(user_agent="ev_locator_app")
user_location_text = st.text_input("📍 Enter your location:")

if user_location_text:
    location = geolocator.geocode(user_location_text)
    if location:
        user_lat, user_lon = location.latitude, location.longitude
        st.success(f"Found location: {location.address} ({user_lat:.4f}, {user_lon:.4f})")

        for station in ev_stations:
            station["distance_km"] = geopy_distance((user_lat, user_lon), (station["lat"], station["lon"])).km
            station["route_url"] = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{station['lat']},{station['lon']}"

        sorted_stations = sorted(ev_stations, key=lambda x: x["distance_km"])

        st.subheader("✅ Closest EV Charging Station")
        closest = sorted_stations[0]
        st.markdown(f"{closest['name']}")
        st.write(f"📍 Location: ({closest['lat']}, {closest['lon']})")
        st.write(f"📏 Distance: {closest['distance_km']:.2f} km")
        st.markdown(f"[🧭 Route to Station]({closest['route_url']})", unsafe_allow_html=True)
