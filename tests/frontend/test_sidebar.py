from unittest.mock import MagicMock

import streamlit as st

from app.streamlit_frontend.components.sidebar import sidebar


def test_sidebar_hidden_when_no_user(mocker):
    mock_sidebar = mocker.patch('streamlit.sidebar')

    sidebar(user=None, nav_items=[], nav_choice=None)

    mock_sidebar.markdown.assert_not_called()
    mock_sidebar.button.assert_not_called()


def test_sidebar_display_with_user(mocker):
    mock_sidebar = mocker.patch('streamlit.sidebar')
    mock_button = MagicMock()
    mock_sidebar.button.return_value = mock_button

    nav_items = ["Dashboard", "Stats"]
    sidebar(user="test_user", nav_items=nav_items, nav_choice="Dashboard")

    mock_sidebar.markdown.assert_any_call("👋 Hello, **test_user**!")

    assert mock_sidebar.button.call_count == 3
    mock_sidebar.button.assert_any_call("Dashboard", key="nav_Dashboard", use_container_width=True)
    mock_sidebar.button.assert_any_call("Stats", key="nav_Stats", use_container_width=True)
    mock_sidebar.button.assert_any_call("🔴 Logout", key="logout_btn", use_container_width=True)


def test_nav_selection(mocker):
    st.session_state = {}
    mock_rerun = mocker.patch('streamlit.rerun')

    mock_sidebar = mocker.patch('streamlit.sidebar')
    mock_sidebar.button.side_effect = lambda *args, **kwargs: (
        (args[0] == "Dashboard")
    )

    sidebar(user="test_user", nav_items=["Dashboard", "Stats"], nav_choice=None)

    assert st.session_state['nav_choice'] == "Dashboard"
    mock_rerun.assert_not_called()


def test_logout_functionality(mocker):
    st.session_state = {
        'user': 'test_user',
        'user_id': 123,
        'page': 'dashboard'
    }
    mock_rerun = mocker.patch('streamlit.rerun')
    mock_success = mocker.patch('streamlit.success')

    mock_sidebar = mocker.patch('streamlit.sidebar')
    mock_sidebar.button.side_effect = lambda *args, **kwargs: (
        (args[0] == "🔴 Logout")
    )

    sidebar(user="test_user", nav_items=[], nav_choice=None)

    assert st.session_state["user"] is None
    assert st.session_state["user_id"] is None
    assert st.session_state['page'] == 'home'

    mock_success.assert_called_once_with("You have logged out.")
    mock_rerun.assert_called_once()


def test_multiple_nav_clicks(mocker):
    st.session_state = {'nav_choice': 'Stats'}
    mock_sidebar = mocker.patch('streamlit.sidebar')

    mock_sidebar.button.return_value = False

    sidebar(user="test_user", nav_items=["Dashboard", "Stats"], nav_choice="Stats")

    assert st.session_state['nav_choice'] == 'Stats'
