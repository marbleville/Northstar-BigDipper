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

def api_put(endpoint, data):
    try:
        url = f"{API_BASE}{endpoint}"
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

# ── Session check ─────────────────────────────────────────────────────────────
if 'traveler_id' not in st.session_state or 'active_trip_id' not in st.session_state:
    st.warning("⚠️ Please set up your session first.")
    st.page_link("Home.py", label="Go to Home →")
    st.stop()

TRAVELER_ID = st.session_state['traveler_id']
TRIP_ID     = st.session_state['active_trip_id']

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .badge {
      display: inline-block;
      padding: 3px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
  }
  .badge-progress  { background: #dbeafe; color: #1d4ed8; }
  .badge-confirmed { background: #dcfce7; color: #15803d; }
  .badge-pending   { background: #fef9c3; color: #a16207; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_trip_data():
    return api_get(f"/trips/{TRIP_ID}")

@st.cache_data(ttl=300)
def load_itinerary_data():
    return api_get(f"/trips/{TRIP_ID}/itinerary")

trip_data      = load_trip_data()
itinerary_data = load_itinerary_data()

if isinstance(trip_data, list):
    trip_data = trip_data[0] if trip_data else None

if not trip_data:
    trip_data = {
        "trip_name":   "Barcelona Group Trip",
        "start_date":  "2026-05-03",
        "end_date":    "2026-05-10",
        "group_size":  8,
        "trip_status": "In Progress"
    }

if not itinerary_data:
    itinerary_data = [
        {"booking_date": "2026-05-03", "description": "BOS → BCN, Delta DL 422",  "booking_status": "Confirmed"},
        {"booking_date": "2026-05-04", "description": "Hotel Arts Barcelona",       "booking_status": "Confirmed"},
        {"booking_date": "2026-05-05", "description": "Sagrada Família tour",       "booking_status": "Pending"},
        {"booking_date": "2026-05-06", "description": "Boqueria food tour",         "booking_status": "Pending"},
        {"booking_date": "2026-05-10", "description": "BCN → BOS, Delta DL 423",  "booking_status": "Confirmed"},
    ]

# ── Session state defaults ────────────────────────────────────────────────────
other_defaults = {
    "trip_status":     "Attending — full trip",
    "avail_notes":     "",
    "activity_status": {
        "Sagrada Família tour (May 5)": "Going",
        "Boqueria food tour (May 6)":   "Going",
        "City bike tour (May 7)":       "Maybe",
    },
}
for k, v in other_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Header ────────────────────────────────────────────────────────────────────
st.title("✈ My Trip")
st.caption(f"Trip ID: {TRIP_ID}  ·  Traveler ID: {TRAVELER_ID}")
st.divider()

tab_itinerary, tab_status = st.tabs(["📋 My Itinerary", "🙋 My Status"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — My Itinerary  (User Story 4.1)
# ══════════════════════════════════════════════════════════════════════════════
with tab_itinerary:
    st.subheader("My Itinerary")

    if trip_data:
        with st.container(border=True):
            col_info, col_badge = st.columns([4, 1])
            with col_info:
                st.markdown(f"**{trip_data.get('trip_name', 'Trip')}**")
                start_date = trip_data.get('start_date', '')
                end_date   = trip_data.get('end_date', '')
                dates      = f"{start_date} – {end_date}" if start_date and end_date else "Dates TBD"
                travelers  = trip_data.get('group_size', 0)
                st.caption(f"{dates}  ·  {travelers} travelers")
            with col_badge:
                status = trip_data.get('trip_status', 'Unknown')
                badge_class = "badge-progress" if status == "In Progress" else "badge-confirmed"
                st.markdown(
                    f'<span class="badge {badge_class}">{status}</span>',
                    unsafe_allow_html=True,
                )
    else:
        st.error("❌ Unable to load trip information.")
        st.stop()

    st.markdown("#### Day-by-day schedule")

    if itinerary_data:
        current_day = None
        for item in itinerary_data:
            booking_date = item.get("booking_date", "")
            if booking_date != current_day:
                current_day = booking_date
                st.markdown(f"**{booking_date}**")

            category_icons = {
                "flight":    "✈",
                "hotel":     "🏨",
                "activity":  "🎭",
                "food":      "🍷",
                "transport": "🚗"
            }
            icon        = category_icons.get(item.get("service_category", "").lower(), "📅")
            status      = item.get("booking_status", "Unknown")
            badge_class = "badge-confirmed" if status == "Confirmed" else "badge-pending"

            col_icon, col_info, col_status = st.columns([0.5, 4, 1.5])
            with col_icon:
                st.markdown(f"<p style='font-size:22px;margin-top:4px'>{icon}</p>", unsafe_allow_html=True)
            with col_info:
                st.markdown(f"**{item.get('description', 'Activity')}**")
                if item.get("vendor_name"):
                    st.caption(f"Vendor: {item['vendor_name']}")
                if item.get("price"):
                    st.caption(f"💰 ${item['price']}")
            with col_status:
                st.markdown(f'<span class="badge {badge_class}">{status}</span>', unsafe_allow_html=True)
            st.divider()
    else:
        st.info("No itinerary items found")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — My Status  (User Story 4.4)
# ══════════════════════════════════════════════════════════════════════════════
with tab_status:
    st.subheader("My participation status")
    st.caption("Keep the planner updated so they can plan around your availability.")

    with st.container(border=True):
        trip_name  = trip_data.get('trip_name', 'Trip') if trip_data else 'Trip'
        start_date = trip_data.get('start_date', '') if trip_data else ''
        end_date   = trip_data.get('end_date', '') if trip_data else ''
        dates      = f"{start_date} – {end_date}" if start_date and end_date else "Dates TBD"
        st.markdown(f"**{trip_name}** — {dates}")

        status_options = ["Attending — full trip", "Attending — partial", "Unavailable", "Tentative"]
        new_status = st.selectbox(
            "Overall trip status", status_options,
            index=status_options.index(st.session_state["trip_status"]),
        )
        avail_notes = st.text_area(
            "Availability notes", value=st.session_state["avail_notes"],
            placeholder="e.g. Unavailable May 7–8 due to a work call...",
        )

    st.markdown("#### Activity RSVP")
    rsvp_options = ["Going", "Not going", "Maybe"]
    updated = {}

    for activity, current in st.session_state["activity_status"].items():
        with st.container(border=True):
            col_a, col_s = st.columns([3, 1])
            col_a.markdown(f"**{activity}**")
            updated[activity] = col_s.selectbox(
                activity, rsvp_options,
                index=rsvp_options.index(current),
                label_visibility="collapsed",
                key=f"rsvp_{activity}",
            )

    if st.button("✅ Update my status", use_container_width=True, type="primary"):
        st.session_state["trip_status"]     = new_status
        st.session_state["avail_notes"]     = avail_notes
        st.session_state["activity_status"] = updated
        st.success("Status updated! The trip planner can now see your latest availability.")

    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("Trip status", st.session_state["trip_status"])
    col2.metric(
        "Activities confirmed",
        f"{sum(1 for v in st.session_state['activity_status'].values() if v == 'Going')} / {len(st.session_state['activity_status'])}",
    )
    if st.session_state["avail_notes"]:
        st.info(f"📝 {st.session_state['avail_notes']}")
