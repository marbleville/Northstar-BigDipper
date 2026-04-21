import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks(show_home=True)

st.title("✈ Big Dipper")
st.subheader("A data-driven Travel Agency Management Platform")

st.divider()

st.markdown("""
Big Dipper connects travelers, planners, agency managers, and vendors into a single unified system.
Trip planning today is fragmented across emails, spreadsheets, and third-party booking tools.
Big Dipper centralizes traveler preferences, vendor inventory, and booking workflows —
enabling planners to design personalized trips efficiently while giving managers real visibility into operations.
""")

st.divider()

st.header("👥 User Personas")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 📋 Juliet O'Hara — Planner")
        st.caption("Trip planning & itinerary management")
        st.write(
            "Juliet is a trip planner at a mid-sized travel agency. "
            "She uses Big Dipper to build itineraries, compare lodging and activity options, "
            "track budgets, and coordinate trips for groups with different preferences — all from one place."
        )

    with st.container(border=True):
        st.markdown("### 📊 Karen Vick — Manager")
        st.caption("Operations & data oversight")
        st.write(
            "Karen is an agency manager who oversees platform usage, vendor activity, "
            "and booking trends. Big Dipper gives her dashboard-level visibility into "
            "demand, vendor performance, and spending patterns, as well as tools to "
            "maintain data quality across the platform."
        )

with col2:
    with st.container(border=True):
        st.markdown("### 🏨 Burton Guster — Vendor")
        st.caption("Listings & promotions management")
        st.write(
            "Burton manages listings for a boutique hotel and tour company. "
            "He uses Big Dipper to keep his offerings accurate and visible to planners, "
            "track booking demand and engagement trends, and create promotional packages "
            "to attract more business."
        )

    with st.container(border=True):
        st.markdown("### 🌍 Shawn Spencer — Traveler")
        st.caption("Trip participation & preferences")
        st.write(
            "Shawn is a traveler who joins trips planned by others but wants meaningful input. "
            "Big Dipper helps him view his itinerary, submit food and lodging preferences, "
            "vote on proposed activities, save listings for later, and stay informed "
            "through real-time trip notifications."
        )

st.divider()

st.header("🛠 Tech Stack")

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Frontend", "Streamlit")
col_b.metric("Backend", "Flask")
col_c.metric("Database", "MySQL 9")
col_d.metric("Infrastructure", "Docker")

st.divider()

st.header("👨‍💻 Team — NorthStar Travelers")

team = [
    ("Laurence Ehrhardt", "Point Person", "ehrhardt.l@northeastern.edu"),
    ("Gaurav Koratagere", "Traveler Persona", "koratagere.g@northeastern.edu"),
    ("Kavya Karthik", "Planner Persona", "karthik.ka@northeastern.edu"),
    ("Simon Coleman", "Manager Persona", "coleman.si@northeastern.edu"),
    ("Gabrielle Tugano", "Vendor Persona", "tugano.g@northeastern.edu"),
]

for name, role, email in team:
    col_name, col_role, col_email = st.columns([2, 2, 3])
    col_name.write(f"**{name}**")
    col_role.write(role)
    col_email.write(email)

st.divider()
st.caption("CS 3200 · Northeastern University · Spring 2026")