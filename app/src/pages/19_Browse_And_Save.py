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

def api_delete(endpoint, data):
    try:
        url = f"{API_BASE}{endpoint}"
        response = requests.delete(url, json=data)
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

# ── Load Data ─────────────────────────────────────────────────────────────────
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
            if description and vote.get("vote_value"):
                vote_counts[description] = vote_counts.get(description, 0) + 1
        return vote_counts
    return {}

votes_data    = load_votes_data()
listings_data = load_listings_data()
vote_counts   = load_vote_counts()
saves_data    = load_saves_data()

# ── Session state ─────────────────────────────────────────────────────────────
if "saves_loaded" not in st.session_state:
    saved_names = {s.get("description") for s in (saves_data or [])}
    st.session_state["saved"] = saved_names
    st.session_state["saves_loaded"] = True

if "voted" not in st.session_state:
    st.session_state["voted"] = set()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🔍 Browse & Save")
st.caption("Vote (♥) on options you like or save (🔖) them for later — the planner sees both.")
st.divider()

# ── Browse listings ───────────────────────────────────────────────────────────
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
                    delete_result = api_delete(f"/trips/{TRIP_ID}/votes", {
                        "items": [{"traveler_id": TRAVELER_ID, "listing_id": listing_id}]
                    })
                    if delete_result is not None:
                        st.success("Vote removed!")
                        load_vote_counts.clear()
                        load_votes_data.clear()
                        st.rerun()
                    else:
                        st.error("Failed to remove vote")
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
