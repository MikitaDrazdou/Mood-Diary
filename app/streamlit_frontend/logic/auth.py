import streamlit as st
import requests
from app.streamlit_frontend.utils import API_URL, get_user_id_from_login_response, set_page

def register():
    st.subheader("Register")
    username = st.text_input("Username", key="reg_user")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    error_box = st.empty()  # Контейнер для ошибок
    if st.button("Sign Up", key="reg_btn"):
        resp = requests.post(f"{API_URL}/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        if resp.status_code == 201:
            user_id = get_user_id_from_login_response(resp)
            if user_id:
                st.session_state["user_id"] = user_id
            st.success("Registration successful! Please log in.")
            set_page('login')
        else:
            try:
                error = resp.json()
                if isinstance(error, list) and error:
                    for e in error:
                        loc = e.get('loc', ['field'])[-1]
                        msg = e.get('msg', 'Invalid input')
                        error_box.error(f"{loc.capitalize()}: {msg}")
                elif isinstance(error, dict) and "detail" in error:
                    error_box.error(error["detail"])
                elif isinstance(error, str):
                    error_box.error(error)
                else:
                    error_box.error(str(error))
            except Exception:
                error_box.error("Registration failed. Please try again.")

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    error_box = st.empty()  # Контейнер для ошибок
    if st.button("Log In", key="login_btn"):
        resp = requests.post(f"{API_URL}/login", json={
            "username": username,
            "password": password
        })
        if resp.status_code == 200:
            st.session_state["user"] = username
            user_id = get_user_id_from_login_response(resp)
            if user_id:
                st.session_state["user_id"] = user_id
            st.success("Login successful!")
            set_page('dashboard')
        else:
            try:
                error = resp.json()
                if isinstance(error, list) and error:
                    for e in error:
                        loc = e.get('loc', ['field'])[-1]
                        msg = e.get('msg', 'Invalid input')
                        error_box.error(f"{loc.capitalize()}: {msg}")
                elif isinstance(error, dict) and "detail" in error:
                    error_box.error(error["detail"])
                elif isinstance(error, str):
                    error_box.error(error)
                else:
                    error_box.error(str(error))
            except Exception:
                error_box.error("Login failed. Please try again.") 