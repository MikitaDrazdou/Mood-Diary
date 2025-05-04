import streamlit as st
import pandas as pd
import requests
import altair as alt
from app.streamlit_frontend.utils import API_URL

def show_calendar(user_id):
    st.subheader("📅 Mood Calendar")
    today = pd.Timestamp.today()
    year = today.year
    month = today.month
    resp = requests.get(f"{API_URL}/mood-entries/{user_id}/{year}/{month}")
    if resp.status_code == 200:
        entries = resp.json()
        if entries:
            df = pd.DataFrame({
                "created_at": [e.get('created_at', e['date']) for e in entries],
                "mood": [e['mood_score'] for e in entries],
                "emoji": [e['emoji'] for e in entries]
            })
            df['created_at'] = pd.to_datetime(df['created_at'])
            # Format for display: 'Apr 27, 2024, 14:35'
            df['created_at_display'] = df['created_at'].dt.strftime('%b %d, %Y, %H:%M')
            chart = (
                alt.Chart(df)
                .mark_line(point=True)
                .encode(
                    x=alt.X('created_at:T', title='Date & Time'),
                    y=alt.Y('mood:Q', scale=alt.Scale(domain=[0, 10]), title='Mood Score'),
                    tooltip=['created_at_display', 'mood', 'emoji']
                )
                .properties(width='container', height=300)
            )
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(
                df.sort_values('created_at', ascending=False)[['created_at_display', 'mood', 'emoji']]
                .rename(columns={"created_at_display": "Date & Time"}),
                use_container_width=True
            )
        else:
            st.info("No entries for this month.")
    else:
        st.error("Error loading calendar.") 