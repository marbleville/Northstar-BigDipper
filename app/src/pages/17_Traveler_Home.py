import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

def api_get(endpoint, params=None):
    try:
        url = f"{API_BASE}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

# ── Traveler ID Input ─────────────────────────────────────────────────────────
st.title("✈ Big Dipper")
st.write("### Welcome, Traveler!")
st.divider()

st.header("🔑 Setup Your Session")

traveler_id_input = st.number_input(
    "Enter your Traveler ID:",
    min_value=1,
    value=1,
    step=1,
    help="This should match a traveler in your database"
)

if st.button("Load My Trips", type="primary", use_container_width=True):
    st.session_state['traveler_id'] = traveler_id_input
    if 'active_trip_id' in st.session_state:
        del st.session_state['active_trip_id']
    for key in ["pref_interests", "pref_accom", "pref_dietary", "prefs_loaded", "saves_loaded"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

if 'traveler_id' not in st.session_state:
    st.info("👆 Please enter your Traveler ID above, then click 'Load My Trips'")
    st.stop()

st.session_state['authenticated'] = True
st.session_state['role'] = 'traveler'

TRAVELER_ID = st.session_state['traveler_id']

# ── Load Traveler Info ────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_traveler_info():
    return api_get(f"/travelers/{TRAVELER_ID}")

traveler_info = load_traveler_info()
if isinstance(traveler_info, list):
    traveler_info = traveler_info[0] if traveler_info else None

if traveler_info:
    traveler_name = f"{traveler_info['first_name']} {traveler_info['last_name']}"
else:
    traveler_name = f"Traveler {TRAVELER_ID}"

st.success(f"✅ Logged in as **{traveler_name}**")

# ── Load Trips ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_traveler_trips():
    return api_get(f"/travelers/{TRAVELER_ID}/trips")

traveler_trips = load_traveler_trips()

if not traveler_trips:
    st.error("❌ No trips found for this traveler ID. Please check your Traveler ID.")
    st.stop()

# ── Trip Selection ────────────────────────────────────────────────────────────
st.header("🎯 Select Your Trip")

if len(traveler_trips) == 1:
    selected_trip = traveler_trips[0]
    st.success(f"✅ Found 1 trip: **{selected_trip['trip_name']}**")
else:
    trip_options = [f"{trip['trip_name']} ({trip['destination']})" for trip in traveler_trips]
    selected_index = st.selectbox(
        "Choose which trip to view:",
        range(len(trip_options)),
        format_func=lambda i: trip_options[i],
    )
    selected_trip = traveler_trips[selected_index]

if st.button("View This Trip", type="primary", use_container_width=True):
    st.session_state['active_trip_id'] = selected_trip['trip_id']
    for key in ["pref_interests", "pref_accom", "pref_dietary", "prefs_loaded", "saves_loaded"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

if 'active_trip_id' not in st.session_state:
    st.info("👆 Select a trip above, then click 'View This Trip'")
    st.stop()

TRIP_ID = st.session_state['active_trip_id']
st.success(f"✅ Viewing: **{selected_trip['trip_name']}** (ID: {TRIP_ID})")

# ── Navigation to pages ───────────────────────────────────────────────────────
st.divider()
st.header("🗺️ Where do you want to go?")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 📋 My Trip")
        st.caption("View your itinerary and update your participation status")
        if st.button("Open →", key="go_trip", use_container_width=True):
            st.switch_page("pages/18_My_Trip.py")

with col2:
    with st.container(border=True):
        st.markdown("### 🔍 Browse & Save")
        st.caption("Explore listings, vote on options, and save your favorites")
        if st.button("Open →", key="go_browse", use_container_width=True):
            st.switch_page("pages/19_Browse_And_Save.py")

with col3:
    with st.container(border=True):
        st.markdown("### ⚙ Preferences & Alerts")
        st.caption("Manage your travel preferences and view notifications")
        if st.button("Open →", key="go_prefs", use_container_width=True):
            st.switch_page("pages/22_Preferences_And_Notifications.py")
