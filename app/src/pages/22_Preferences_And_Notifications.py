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
  .notif-unread { border-left: 3px solid #ef4444; padding-left: 10px; }
  .notif-read   { border-left: 3px solid #d1d5db; padding-left: 10px; opacity: 0.7; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_preferences_data():
    return api_get(f"/trips/{TRIP_ID}/travelers/{TRAVELER_ID}/preferences")

@st.cache_data(ttl=300)
def load_notifications_data():
    return api_get(f"/travelers/{TRAVELER_ID}/notifications")

preferences_data   = load_preferences_data()
notifications_data = load_notifications_data()

if not isinstance(preferences_data, list):
    preferences_data = []

if not notifications_data:
    notifications_data = []

# ── Parse preferences from DB ─────────────────────────────────────────────────
def parse_preferences_from_db(rows):
    lodging_options  = ["Hotel", "Airbnb", "Resort", "Hostel", "Boutique"]
    food_options     = ["Vegetarian", "Vegan", "Halal", "Gluten-free", "No restrictions"]
    activity_options = ["Food", "Adventure", "Culture", "Nightlife", "Nature", "Shopping", "Wellness", "Luxury"]

    lodging_map  = {o.lower(): o for o in lodging_options}
    food_map     = {o.lower(): o for o in food_options}
    activity_map = {o.lower(): o for o in activity_options}

    food = []
    lodging = []
    activity = []

    for row in (rows or []):
        pref = row.get("preference", "")
        if ":" in pref:
            category, value = pref.split(":", 1)
            value_lower = value.lower()
            if category == "lodging" and value_lower in lodging_map:
                lodging.append(lodging_map[value_lower])
            elif category == "food" and value_lower in food_map:
                food.append(food_map[value_lower])
            elif category == "activity" and value_lower in activity_map:
                activity.append(activity_map[value_lower])

    return food, lodging, activity

db_food, db_lodging, db_activity = parse_preferences_from_db(preferences_data)

# ── Session state ─────────────────────────────────────────────────────────────
if "prefs_loaded" not in st.session_state:
    st.session_state["pref_dietary"]   = db_food
    st.session_state["pref_accom"]     = db_lodging
    st.session_state["pref_interests"] = db_activity
    st.session_state["prefs_loaded"]   = True

st.session_state["notif_read"] = {
    i: n.get("read_status", False) for i, n in enumerate(notifications_data or [])
}

# ── Header ────────────────────────────────────────────────────────────────────
unread = sum(1 for n in (notifications_data or []) if not n.get("read_status", False))

st.title("⚙ Preferences & Notifications")
st.caption(f"🔔 {unread} unread notification{'s' if unread != 1 else ''}")
st.divider()

tab_prefs, tab_notifs = st.tabs([
    "⚙ Preferences",
    f"🔔 Alerts ({unread})",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Preferences  (User Story 4.2)
# ══════════════════════════════════════════════════════════════════════════════
with tab_prefs:
    st.subheader("Your travel preferences")
    st.caption("Help the planner build a trip that fits you.")

    with st.form("preferences_form"):
        st.markdown("**Interests**")
        pref_interests = st.multiselect(
            "Interests", ["Food", "Adventure", "Culture", "Nightlife", "Nature", "Shopping", "Wellness", "Luxury"],
            default=st.session_state["pref_interests"], label_visibility="collapsed",
        )

        st.markdown("**Accommodation type**")
        pref_accom = st.multiselect(
            "Accommodation", ["Hotel", "Airbnb", "Resort", "Hostel", "Boutique"],
            default=st.session_state["pref_accom"], label_visibility="collapsed",
        )

        st.markdown("**Dietary needs**")
        pref_dietary = st.multiselect(
            "Dietary", ["Vegetarian", "Vegan", "Halal", "Gluten-free", "No restrictions"],
            default=st.session_state["pref_dietary"], label_visibility="collapsed",
        )

        submitted = st.form_submit_button("💾 Save preferences", use_container_width=True)

    if submitted:
        st.session_state["pref_interests"] = pref_interests
        st.session_state["pref_accom"]     = pref_accom
        st.session_state["pref_dietary"]   = pref_dietary

        preferences_payload = {}
        if pref_dietary:
            preferences_payload["food_preferences"] = pref_dietary
        if pref_accom:
            preferences_payload["lodging_preferences"] = pref_accom
        if pref_interests:
            preferences_payload["activity_preferences"] = [i.lower() for i in pref_interests]

        if preferences_payload:
            result = api_put(f"/trips/{TRIP_ID}/travelers/{TRAVELER_ID}/preferences", preferences_payload)
            if result is not None:
                load_preferences_data.clear()
                st.session_state["prefs_loaded"] = False
                st.success("Preferences saved!")
                st.rerun()
            else:
                st.error("Failed to save preferences. Please try again.")
        else:
            st.info("No preferences selected — nothing to save.")

    st.divider()
    st.markdown("#### Current preferences")
    for label, values in [
        ("Interests",      st.session_state["pref_interests"]),
        ("Accommodation",  st.session_state["pref_accom"]),
        ("Dietary needs",  st.session_state["pref_dietary"]),
    ]:
        col_l, col_v = st.columns([1.5, 4])
        col_l.caption(label)
        col_v.write(", ".join(values) if values else "—")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Notifications  (User Story 4.6)
# ══════════════════════════════════════════════════════════════════════════════
with tab_notifs:
    st.subheader("Trip notifications")

    col_btn, _ = st.columns([1, 4])
    if col_btn.button("Mark all read", disabled=unread == 0):
        update_payload = {
            "notification_ids": [n["notification_id"] for n in (notifications_data or [])],
            "read_status": True
        }
        result = api_put(f"/travelers/{TRAVELER_ID}/notifications", update_payload)
        if result is not None:
            load_notifications_data.clear()
            for i in range(len(notifications_data or [])):
                st.session_state["notif_read"][i] = True
            st.rerun()
        else:
            st.error("Failed to mark notifications as read")

    if notifications_data:
        for i, notif in enumerate(notifications_data):
            is_read   = st.session_state["notif_read"].get(i, notif.get("read_status", False))
            css_class = "notif-read" if is_read else "notif-unread"

            with st.container(border=True):
                col_msg, col_action = st.columns([5, 1])
                with col_msg:
                    st.markdown(
                        f'<div class="{css_class}"><strong>{"" if is_read else "🔴 "}{notif.get("message", "")}</strong></div>',
                        unsafe_allow_html=True,
                    )
                    created_date = notif.get("created_date", "")
                    st.caption("Recently" if (created_date and not is_read) else "Earlier")
                with col_action:
                    if not is_read:
                        if st.button("Read", key=f"read_{i}"):
                            update_payload = {
                                "notification_ids": [notif["notification_id"]],
                                "read_status": True
                            }
                            result = api_put(f"/travelers/{TRAVELER_ID}/notifications", update_payload)
                            if result is not None:
                                load_notifications_data.clear()
                                st.session_state["notif_read"][i] = True
                                st.rerun()
                            else:
                                st.error("Failed to mark notification as read")
                    else:
                        st.caption("✓ Read")
    else:
        st.info("No notifications found")
