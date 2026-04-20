import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

st.set_page_config(page_title="Vendor Hub", layout="wide")
SideBarLinks()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro&display=swap');
    html, body, [class*="css"] {
        font-family: 'Source Code Pro', monospace;
    }
    div.stButton > button {
        background-color: purple;
        color: white;
        font-family: 'Source Code Pro', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Mock data --------------------------------------------------------------
if "listings" not in st.session_state:
    st.session_state.listings = [
        {"name": "Spring Break Package",  "status": "Active",   "price": 299, "availability": "Mar–Apr"},
        {"name": "Large Group Catering",  "status": "Active",   "price": 850, "availability": "Year-round"},
        {"name": "Summer Retreat Bundle", "status": "Inactive", "price": 450, "availability": "Jun–Aug"},
    ]

if "bookings" not in st.session_state:
    st.session_state.bookings = [
        {"group": "$$$ Travel Group", "status": "Pending"},
        {"group": "YYY Event Co.",    "status": "Confirmed"},
        {"group": "Miami Tour",       "status": "Confirmed"},
        {"group": "$$$ Corp Retreat", "status": "Pending"},
    ]

if "promotions" not in st.session_state:
    st.session_state.promotions = [
        {"name": "Spring Break Package", "active": True},
        {"name": "Large Group Catering", "active": False},
    ]

engagement = {"Sun": 50, "Mon": 85, "Tue": 40, "Wed": 50, "Thu": 20, "Fri": 80, "Sat": 100}

# ---- Header -----------------------------------------------------------------
st.title("Vendor Hub")
st.caption(f"Welcome back, {st.session_state.get('first_name', 'Gus')} 👋")

# ---- Metrics ----------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Listings", sum(1 for l in st.session_state.listings if l["status"] == "Active"))
col2.metric("Bookings",        len(st.session_state.bookings))
col3.metric("Avg Engagement",  f"{round(sum(engagement.values()) / len(engagement))}%")
col4.metric("Promotions",      sum(1 for p in st.session_state.promotions if p["active"]))

st.divider()

# ---- Tabs -------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📋 My Listings", "📊 Bookings & Engagement", "🎁 Promotions", "➕ Add Listing"])

# ---- Tab 1: My Listings -----------------------------------------------------
with tab1:
    st.subheader("All Listings")
    for i, listing in enumerate(st.session_state.listings):
        with st.expander(f"{listing['name']}  —  {listing['status']}"):
            new_name   = st.text_input("Listing Name",  listing["name"],         key=f"name_{i}")
            new_price  = st.number_input("Price ($)",   value=listing["price"],  key=f"price_{i}")
            new_avail  = st.text_input("Availability",  listing["availability"], key=f"avail_{i}")
            new_status = st.selectbox("Status", ["Active", "Inactive"],
                                      index=0 if listing["status"] == "Active" else 1,
                                      key=f"status_{i}")
            st.text_area("Amenities / Notes", key=f"amenities_{i}",
                         placeholder="e.g. WiFi, Catering, AV equipment...")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Save Changes", key=f"save_{i}", use_container_width=True):
                    st.session_state.listings[i] = {
                        "name": new_name, "price": new_price,
                        "availability": new_avail, "status": new_status,
                    }
                    st.success("Listing updated!")
            with c2:
                if st.button("Mark Inactive", key=f"deactivate_{i}", use_container_width=True):
                    st.session_state.listings[i]["status"] = "Inactive"
                    st.warning(f"'{listing['name']}' marked inactive.")

# ---- Tab 2: Bookings & Engagement -------------------------------------------
with tab2:
    left, right = st.columns(2)

    with left:
        st.subheader("Recent Booking Requests")
        icons = {"Pending": "🟡", "Confirmed": "🟢", "Declined": "🔴"}
        for b in st.session_state.bookings:
            st.markdown(f"{icons.get(b['status'], '⚪')} **{b['group']}** — {b['status']}")

    with right:
        st.subheader("Engagement Trends")
        eng_df = pd.DataFrame({"Day": list(engagement.keys()), "Views": list(engagement.values())})
        st.bar_chart(eng_df.set_index("Day"))

# ---- Tab 3: Promotions ------------------------------------------------------
with tab3:
    st.subheader("Active Promotions")
    for j, promo in enumerate(st.session_state.promotions):
        pc1, pc2 = st.columns([3, 1])
        pc1.write(f"{'🟢' if promo['active'] else '⚫'} {promo['name']}")
        with pc2:
            if st.button("Disable" if promo["active"] else "Enable",
                         key=f"promo_{j}", use_container_width=True):
                st.session_state.promotions[j]["active"] = not promo["active"]
                st.rerun()

    st.divider()
    st.subheader("Create Promotion")
    with st.form("new_promo_form"):
        p_name = st.text_input("Promotion Name")
        st.text_area("Details (dates, discount, group size...)")
        if st.form_submit_button("Create Promotion", use_container_width=True) and p_name:
            st.session_state.promotions.append({"name": p_name, "active": True})
            st.success(f"Promotion '{p_name}' created!")

# ---- Tab 4: Add Listing -----------------------------------------------------
with tab4:
    st.subheader("Add New Listing")
    st.caption("Listings > Add New Listing")

    with st.form("add_listing_form"):

        # Service Details
        st.subheader("Service Details")
        listing_name = st.text_input("Listing Name", placeholder="e.g. XX Boutique Hotel")
        service_type = st.selectbox("Service Type", ["Select Type", "Venue", "Catering", "Transport", "Activity", "Other"])
        description  = st.text_area("Description", placeholder="Describe your service for planners and travelers...")

        st.divider()

        # Pricing
        st.subheader("Pricing")
        p1, p2 = st.columns(2)
        with p1:
            base_price = st.number_input("Base Price ($)", min_value=0.0, format="%.2f")
        with p2:
            price_per  = st.selectbox("Price Per", ["per night", "per person", "per event", "flat rate"])
        group_pricing = st.radio("Group Pricing Available?", ["Yes", "No"], horizontal=True)

        st.divider()

        # Availability
        st.subheader("Availability")
        a1, a2 = st.columns(2)
        with a1:
            avail_from = st.date_input("Available From")
        with a2:
            avail_to   = st.date_input("Available To")

        h1, h2 = st.columns(2)
        with h1:
            opens  = st.text_input("Operating Hours — Opens",  placeholder="Opens 9AM")
        with h2:
            closes = st.text_input("Operating Hours — Closes", placeholder="Closes 5PM")

        st.write("Days Available")
        day_cols = st.columns(7)
        days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
        [day_cols[i].checkbox(days[i], key=f"day_{i}") for i in range(7)]

        st.divider()

        # Amenities and Notes
        st.subheader("Amenities and Notes")
        st.write("Amenities (select all that apply)")
        am1, am2, am3, am4 = st.columns(4)
        am1.checkbox("WiFi",      key="wifi")
        am2.checkbox("Parking",   key="parking")
        am3.checkbox("Breakfast", key="breakfast")
        custom_amenity = am4.text_input("+ Add more", placeholder="e.g. Pool")

        promo_notes = st.text_input("Promotional Discounts",
                                    placeholder="e.g. Spring Break Discount, Large Group Deal...")

        st.divider()

        submitted = st.form_submit_button("Submit Listing", use_container_width=True)
        if submitted:
            if not listing_name or service_type == "Select Type":
                st.error("Please fill in at least a listing name and service type.")
            else:
                st.session_state.listings.append({
                    "name":         listing_name,
                    "status":       "Active",
                    "price":        base_price,
                    "availability": f"{avail_from} – {avail_to}",
                })
                st.success(f"'{listing_name}' has been submitted and is now active!")