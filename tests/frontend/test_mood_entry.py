from datetime import date

from app.streamlit_frontend.components.mood_entry_form import add_mood


def test_mood_entry_submission(mocker, mock_requests):
    mock_date = mocker.patch('datetime.date')
    mock_date.today.return_value = date(2025, 5, 5)

    mocker.patch('streamlit.button', return_value=True)
    mocker.patch('streamlit.slider', return_value=7)
    mocker.patch('streamlit.selectbox', return_value="😀")
    mocker.patch('streamlit.text_area', return_value="Test notes")
    mocker.patch('streamlit.text_input', return_value="running,swimming")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_requests.return_value = mock_response

    add_mood(user_id=1)

    mock_requests.assert_called_once_with(
        "http://localhost:8000/mood-entry",
        json={
            "date": "2025-05-05",
            "mood_score": 7,
            "emoji": "😀",
            "notes": "Test notes",
            "activities": "running,swimming"
        },
        params={"user_id": 1}
    )
