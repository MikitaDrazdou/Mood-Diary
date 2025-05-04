import streamlit as st
from app.streamlit_frontend.components.sidebar import sidebar
from app.streamlit_frontend.components.mood_entry_form import add_mood
from app.streamlit_frontend.logic.calendar import show_calendar
from app.streamlit_frontend.logic.stats import show_stats

def dashboard():
    user = st.session_state['user']
    nav_items = ["Add Entry", "Calendar", "Statistics"]
    nav_choice = st.session_state.get('nav_choice', nav_items[0])
    sidebar(user, nav_items, nav_choice)
    if nav_choice == "Add Entry":
        add_mood(st.session_state["user_id"])
    elif nav_choice == "Calendar":
        show_calendar(st.session_state["user_id"])
    elif nav_choice == "Statistics":
        show_stats(st.session_state["user_id"]) 