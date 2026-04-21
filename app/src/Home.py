##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
from modules.nav import SideBarLinks
import streamlit as st
import logging
logging.basicConfig(
    format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


st.set_page_config(layout='wide')

st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")
st.title('Big Dipper 🧭')
st.write('#### Hi! As which user would you like to log in?')

if st.button('Act as Karen Vick, a Manager',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'manager'
    st.session_state['first_name'] = 'Karen'
    st.switch_page('pages/50_Manager_Home.py')

if st.button('Act as Shawn, a Traveler',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'traveler'
    st.session_state['first_name'] = 'Shawn'
    # Don't switch page yet - let the traveler page handle user ID input
    st.switch_page('pages/17_Traveler_Home.py')

if st.button("Act as Gus, a Vendor",
             type='primary',
             use_container_width=True):
    st.session_state["authenticated"] = True
    # must match what you put in nav.py
    st.session_state["role"] = "burton_guster"
    st.switch_page("pages/01_Vendor.py")

if st.button('Act as Juliet, a Trip Planner',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'planner'
    st.session_state['first_name'] = 'Juliet'
    st.session_state['user_id'] = 1
    logger.info("Logging in as Planner Persona")
    st.switch_page('pages/40_Planner_Home.py')
