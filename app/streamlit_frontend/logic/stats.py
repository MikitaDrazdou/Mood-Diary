import streamlit as st
import requests
from app.streamlit_frontend.utils import API_URL

def show_stats(user_id):
    st.markdown("""
        <h2 style='font-size:2rem; margin-bottom:1.5em;'>📊 Mood Statistics</h2>
    """, unsafe_allow_html=True)
    resp = requests.get(f"{API_URL}/stats/{user_id}")
    if resp.status_code == 200:
        stats = resp.json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Entries", stats['total_entries'])
        col2.metric("Average Mood", f"{stats['avg_score']:.2f}")
        col3.metric("Max", stats['max_score'])
        col4.metric("Min", stats['min_score'])
        st.markdown("---")
        st.subheader("Top Emojis")
        if stats['emoji_counts']:
            emoji_counts = stats['emoji_counts']
            for emoji, count in emoji_counts.items():
                st.write(f"<span style='font-size:2em;'>{emoji}</span> — <b>{count}</b> times", unsafe_allow_html=True)
        else:
            st.info("No emoji data.")
        st.markdown("---")
        st.subheader("Top Activities")
        if stats['top_activities']:
            for activity, count in stats['top_activities']:
                st.progress(count, text=activity)
        else:
            st.info("No activity data.")
    else:
        st.error("Error loading statistics") 