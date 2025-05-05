from unittest.mock import call

import pytest
import streamlit as st

from app.streamlit_frontend.logic.auth import register, login


@pytest.fixture(autouse=True)
def mock_session(mocker):
    mocker.patch('streamlit.session_state', {})
    mocker.patch('streamlit.button')
    mocker.patch('streamlit.text_input')
    mocker.patch('streamlit.empty')
    mocker.patch('streamlit.success')
    mocker.patch('streamlit.rerun')
    mocker.patch('app.streamlit_frontend.utils.set_page')


def test_register_success(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"user_id": 123}
    mock_post.return_value = mock_response

    register()

    assert st.session_state["user_id"] == 123
    st.success.assert_called_with("Registration successful! Please log in.")
    st.rerun.assert_called_once()


def test_register_detail_error(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"detail": "Username taken"}
    mock_post.return_value = mock_response

    register()

    st.empty().error.assert_called_with("Username taken")


def test_register_string_error(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = "Invalid request"
    mock_post.return_value = mock_response

    register()

    st.empty().error.assert_called_with("Invalid request")


def test_login_success(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"user_id": 456}
    mock_post.return_value = mock_response

    login()

    assert st.session_state["user"] == st.text_input.return_value
    assert st.session_state["user_id"] == 456
    st.success.assert_called_with("Login successful!")
    st.rerun.assert_called_once()


def test_login_detail_error(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {"detail": "Invalid credentials"}
    mock_post.return_value = mock_response

    login()

    st.empty().error.assert_called_with("Invalid credentials")


def test_login_multiple_errors(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 422
    mock_response.json.return_value = [
        {"loc": ["username"], "msg": "Required field"},
        {"loc": ["password"], "msg": "Minimum 8 characters"}
    ]
    mock_post.return_value = mock_response

    login()

    assert st.empty().error.call_count == 2
    st.empty().error.assert_has_calls([
        call("Username: Required field"),
        call("Password: Minimum 8 characters")
    ])


def test_login_unexpected_error_format(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "Unexpected format"}
    mock_post.return_value = mock_response

    login()

    st.empty().error.assert_called_with("{'error': 'Unexpected format'}")


def test_login_missing_user_id(mocker, mock_post):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_post.return_value = mock_response

    login()

    assert "user_id" not in st.session_state
    st.success.assert_called_with("Login successful!")
