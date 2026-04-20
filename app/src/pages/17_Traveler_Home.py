import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

# ── API Configuration ────────────────────────────────────────────────────────
API_BASE = "http://web-api:4000"

# ── API Helper Functions ──────────────────────────────────────────────────────
def api_get(endpoint, params=None):
    try:
        url = f"{API_BASE}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def api_post(endpoint, data):
    try:
        url = f"{API_BASE}{endpoint}"
        response = requests.post(url, json=data)
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

# ── Traveler ID Input ─────────────────────────────────────────────────
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

TRAVELER_ID = st.session_state['traveler_id']

# ── Load Traveler Info ─────────────────────────────────────────────────────
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

st.title(f"Welcome {traveler_name}!")
st.write('### Stay informed and involved in your trips!')

# ── Load Traveler's Trips ────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_traveler_trips():
    return api_get(f"/travelers/{TRAVELER_ID}/trips")

traveler_trips = load_traveler_trips()

if not traveler_trips:
    st.error("❌ No trips found for this traveler ID. Please check your Traveler ID.")
    st.stop()

# ── Trip Selection ──────────────────────────────────────────────────────────
st.header("🎯 Select Your Trip")

if len(traveler_trips) == 1:
    selected_trip = traveler_trips[0]
    st.success(f"✅ Found 1 trip for you: **{selected_trip['trip_name']}**")
else:
    trip_options = [f"{trip['trip_name']} ({trip['destination']})" for trip in traveler_trips]

    selected_index = st.selectbox(
        "Choose which trip to view:",
        range(len(trip_options)),
        format_func=lambda i: trip_options[i],
        help="Select the trip you want to manage"
    )
    selected_trip = traveler_trips[selected_index]

if st.button("View This Trip", type="primary"):
    st.session_state['active_trip_id'] = selected_trip['trip_id']
    for key in ["pref_interests", "pref_accom", "pref_dietary", "prefs_loaded", "saves_loaded"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

if 'active_trip_id' not in st.session_state:
    st.info("👆 Please select a trip above, then click 'View This Trip'")
    st.stop()

TRIP_ID = st.session_state['active_trip_id']

st.success(f"✅ Viewing trip: **{selected_trip['trip_name']}** (ID: {TRIP_ID})")

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
  .badge-draft     { background: #f3f4f6; color: #374151; }
  .notif-unread { border-left: 3px solid #ef4444; padding-left: 10px; }
  .notif-read   { border-left: 3px solid #d1d5db; padding-left: 10px; opacity: 0.7; }
</style>
""", unsafe_allow_html=True)

# ── Load Data from APIs ────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_trip_data():
    return api_get(f"/trips/{TRIP_ID}")

@st.cache_data(ttl=300)
def load_itinerary_data():
    return api_get(f"/trips/{TRIP_ID}/itinerary")

@st.cache_data(ttl=300)
def load_notifications_data():
    return api_get(f"/travelers/{TRAVELER_ID}/notifications")

@st.cache_data(ttl=300)
def load_preferences_data():
    return api_get(f"/trips/{TRIP_ID}/travelers/{TRAVELER_ID}/preferences")

@st.cache_data(ttl=300)
def load_votes_data():
    return api_get(f"/trips/{TRIP_ID}/votes")

@st.cache_data(ttl=300)
def load_listings_data():
    return api_get("/listings")

@st.cache_data(ttl=300)
def load_saves_data():
    return api_get(f"/trips/{TRIP_ID}/travelers/{TRAVELER_ID}/saves")

@st.cache_data(ttl=60)
def load_vote_counts():
    votes_data = api_get(f"/trips/{TRIP_ID}/votes")
    if votes_data:
        vote_counts = {}
        for vote in votes_data:
            description = vote.get("description", "")
            if description and vote.get("vote_value"):  # only count TRUE votes
                vote_counts[description] = vote_counts.get(description, 0) + 1
        return vote_counts
    return {}

# ── Load and unwrap API responses ─────────────────────────────────────────────
trip_data          = load_trip_data()
itinerary_data     = load_itinerary_data()
notifications_data = load_notifications_data()
preferences_data   = load_preferences_data()
votes_data         = load_votes_data()
listings_data      = load_listings_data()
vote_counts        = load_vote_counts()
saves_data         = load_saves_data()

if isinstance(trip_data, list):
    trip_data = trip_data[0] if trip_data else None
if not isinstance(preferences_data, list):
    preferences_data = []

# ── Parse preferences from DB ─────────────────────────────────────────────────
# API returns rows like: {"preference": "lodging:Airbnb", "traveler_id": 1, "trip_id": 1}

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

# ── Fallback data if API is unavailable ───────────────────────────────────────
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

if not notifications_data:
    notifications_data = []

# ── Session state initialization ─────────────────────────────────────────────
# Load preferences from DB on first load, not hardcoded defaults
if "prefs_loaded" not in st.session_state:
    st.session_state["pref_dietary"]   = db_food
    st.session_state["pref_accom"]     = db_lodging
    st.session_state["pref_interests"] = db_activity
    st.session_state["prefs_loaded"]   = True

if "saves_loaded" not in st.session_state:
    saved_names = {s.get("description") for s in (saves_data or [])}
    st.session_state["saved"] = saved_names
    st.session_state["saves_loaded"] = True

other_defaults = {
    "trip_status":     "Attending — full trip",
    "avail_notes":     "",
    "activity_status": {
        "Sagrada Família tour (May 5)": "Going",
        "Boqueria food tour (May 6)":   "Going",
        "City bike tour (May 7)":       "Maybe",
    },
    "voted": set(),
    "saved": set(),
    "notif_read": {i: n.get("read_status", False) for i, n in enumerate(notifications_data or [])},
}

for k, v in other_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Header ────────────────────────────────────────────────────────────────────
unread = sum(1 for n in (notifications_data or []) if not n.get("read_status", False))

col_logo, col_notif = st.columns([3, 1])
with col_logo:
    st.markdown("## ✈ Big Dipper")
with col_notif:
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(f"🔔 {unread} unread")

st.divider()

# ── Navigation ────────────────────────────────────────────────────────────────
tab_itinerary, tab_prefs, tab_browse, tab_status, tab_notifs = st.tabs([
    "📋 My Itinerary",
    "⚙ Preferences",
    "🔍 Browse",
    "🙋 My Status",
    f"🔔 Alerts ({unread})",
])

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
        st.error("❌ Unable to load trip information. Please check your connection and try again.")
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
            icon   = category_icons.get(item.get("service_category", "").lower(), "📅")
            status = item.get("booking_status", "Unknown")
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
# TAB 2 — Preferences  (User Story 4.2)
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
# TAB 3 — Browse  (User Stories 4.3 + 4.5)
# ══════════════════════════════════════════════════════════════════════════════
with tab_browse:
    st.subheader("Browse options")
    st.caption("Vote (♥) on options you like or save (🔖) them for later — the planner sees both.")

    browse_items = {"Hotel": [], "Food": [], "Activity": [], "Tour": []}

    if listings_data:
        for listing in listings_data:
            category = listing.get("service_category", "").title()
            if category in browse_items:
                icon_map = {
                    "Hotel":    "🏨",
                    "Food":     "🥘",
                    "Activity": "🎭",
                    "Tour":     "🗺️",
                }
                browse_items[category].append({
                    "icon":       icon_map.get(category, "📅"),
                    "name":       listing.get("description", "Unknown"),
                    "sub":        f"{listing.get('service_category', '')} · {listing.get('vendor_name', 'Unknown vendor')}",
                    "price":      f"${listing.get('price', 0)}",
                    "listing_id": listing.get("listing_id")
                })

    category = st.radio(
        "Category", list(browse_items.keys()),
        horizontal=True, label_visibility="collapsed",
    )

    for item in browse_items.get(category, []):
        name       = item["name"]
        listing_id = item.get("listing_id")

        user_voted = any(
            vote.get("traveler_id") == TRAVELER_ID and vote.get("description") == name
            for vote in (votes_data or [])
        )
        count = vote_counts.get(name, 0)

        with st.container(border=True):
            col_icon, col_info, col_vote, col_save = st.columns([0.5, 4, 1.2, 1.2])

            with col_icon:
                st.markdown(f"<p style='font-size:28px;margin-top:4px'>{item['icon']}</p>", unsafe_allow_html=True)
            with col_info:
                st.markdown(f"**{name}**")
                st.caption(item["sub"])
                st.caption(f"💰 {item['price']}")
            with col_vote:
                vote_label = f"♥ {count}" + (" ✓" if user_voted else "")
                if st.button(vote_label, key=f"vote_{name}", use_container_width=True):
                    if user_voted:
                        st.info("Vote removal not yet implemented")
                    else:
                        if listing_id:
                            vote_result = api_post(f"/trips/{TRIP_ID}/votes", {
                                "traveler_id": TRAVELER_ID,
                                "listing_id":  listing_id,
                                "vote_value":  1
                            })
                            if vote_result is not None:
                                st.success("Vote submitted!")
                                load_vote_counts.clear()
                                load_votes_data.clear()
                                st.rerun()
                            else:
                                st.error("Failed to submit vote")
            with col_save:
                saved = name in st.session_state["saved"]
                if st.button("🔖 Saved" if saved else "🔖 Save", key=f"save_{name}", use_container_width=True):
                    result = api_put(
                        f"/trips/{TRIP_ID}/travelers/{TRAVELER_ID}/votes/{listing_id}/save",
                        {}
                    )
                    if result is not None:
                        if saved:
                            st.session_state["saved"].discard(name)
                        else:
                            st.session_state["saved"].add(name)
                        load_saves_data.clear()
                        st.rerun()
                    else:
                        st.error("Failed to save item")

    st.divider()
    if st.session_state["saved"]:
        with st.expander(f"🔖 Saved items ({len(st.session_state['saved'])})"):
            for s in sorted(st.session_state["saved"]):
                col_n, col_r = st.columns([5, 1])
                col_n.markdown(f"- {s}")
                if col_r.button("✕", key=f"unsave_{s}"):
                    st.session_state["saved"].discard(s)
                    st.rerun()
    else:
        st.caption("No saved items yet.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — My Status  (User Story 4.4)
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

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Notifications  (User Story 4.6)
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