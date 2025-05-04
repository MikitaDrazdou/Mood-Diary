# utils.py — вспомогательные функции для Streamlit frontend

import requests
import streamlit as st

API_URL = "http://localhost:8000"

def get_user_id_from_login_response(resp):
    # Ожидаем, что backend возвращает user_id в ответе на логин/регистрацию
    try:
        data = resp.json()
        return data.get("user_id")
    except Exception:
        return None

def set_page(page: str):
    st.session_state['page'] = page
    st.rerun() 