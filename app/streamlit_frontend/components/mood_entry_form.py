import streamlit as st
import requests
from app.streamlit_frontend.utils import API_URL
import datetime

def add_mood(user_id):
    st.markdown("""
        <h2 style='text-align:center; font-size:2rem; margin-bottom:0.5em;'>
            <span style='font-size:1.5em;'>📝</span> Add Mood Entry
        </h2>
    """, unsafe_allow_html=True)
    today = datetime.date.today()
    mood_score = st.slider("Rate your mood (1-10)", 1, 10, 5, key="mood_slider")
    emoji = st.selectbox("Emoji", ["😀", "🙂", "😐", "🙁", "😢", "😡", "😴", "🤒", "🥰", "😎"], key="mood_emoji")
    notes = st.text_area("Notes", key="mood_notes")
    activities = st.text_input("Activities (comma separated)", key="mood_activities")
    if st.button("Save Entry", key="save_mood"):
        resp = requests.post(f"{API_URL}/mood-entry", json={
            "date": str(today),
            "mood_score": mood_score,
            "emoji": emoji,
            "notes": notes,
            "activities": activities
        }, params={"user_id": user_id})
        if resp.status_code == 200:
            st.success("Entry saved!")
        else:
            st.error("Error saving entry") 