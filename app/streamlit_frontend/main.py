import streamlit as st
from app.streamlit_frontend.logic.auth import login, register
from app.streamlit_frontend.logic.dashboard import dashboard

def main():
    st.set_page_config(page_title="Mood Diary", page_icon="📔", layout="centered")
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'
    # Красивая шапка страницы
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #f8fafc 0%, #e0e7ef 100%); padding: 2.5rem 1rem 1.5rem 1rem; border-radius: 1.5rem; margin-bottom: 2rem; box-shadow: 0 2px 16px 0 rgba(0,0,0,0.04);">
            <h1 style="text-align: center; font-size: 2.8rem; margin-bottom: 0.5rem; color: #2d3748; letter-spacing: 1px; font-family: 'Segoe UI', 'Arial', sans-serif;">
                📔 Mood Diary
            </h1>
            <div style="text-align: center; font-size: 1.25rem; color: #4a5568; font-family: 'Segoe UI', 'Arial', sans-serif;">
                Track your mood and analyze your emotions!
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if not st.session_state["user"]:
        with st.sidebar:
            st.markdown("### Account")
            if st.button("Log In", key="login_sidebar_btn", use_container_width=True):
                st.session_state['page'] = 'login'
            if st.button("Sign Up", key="signup_sidebar_btn", use_container_width=True):
                st.session_state['page'] = 'register'
        if st.session_state['page'] == 'login':
            login()
        elif st.session_state['page'] == 'register':
            register()
    else:
        dashboard()

if __name__ == "__main__":
    main() 