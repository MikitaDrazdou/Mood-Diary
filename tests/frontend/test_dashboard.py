import pytest
import streamlit as st

from app.streamlit_frontend.logic.dashboard import dashboard


@pytest.fixture
def mock_dependencies(mocker):
    return {
        'sidebar': mocker.patch('app.streamlit_frontend.components.sidebar.sidebar'),
        'add_mood': mocker.patch('app.streamlit_frontend.components.mood_entry_form.add_mood'),
        'show_calendar': mocker.patch('app.streamlit_frontend.logic.calendar.show_calendar'),
        'show_stats': mocker.patch('app.streamlit_frontend.logic.stats.show_stats'),
    }


def test_session_state_safety(mock_dependencies):
    st.session_state.clear()
    st.session_state['user'] = 'temp_user'

    with pytest.raises(KeyError):
        dashboard()

    mock_dependencies['sidebar'].assert_not_called()
