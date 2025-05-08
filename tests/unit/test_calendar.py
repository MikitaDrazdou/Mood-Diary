from unittest.mock import Mock

from app.streamlit_frontend.logic.calendar import show_calendar


def test_calendar_data_processing(mocker):
    mock_response = Mock(
        status_code=200,
        json=lambda: [{
            "date": "2024-01-01",
            "mood_score": 8,
            "emoji": "😀",
            "created_at": "2024-01-01T12:00:00"
        }]
    )
    mocker.patch('requests.get', return_value=mock_response)
    mock_st = mocker.patch('streamlit.altair_chart')

    show_calendar(user_id=1)

    assert mock_st.call_count == 1
