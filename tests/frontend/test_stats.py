from app.streamlit_frontend.logic.stats import show_stats


def test_stats_rendering(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "total_entries": 10,
        "avg_score": 7.5,
        "max_score": 9,
        "min_score": 5,
        "emoji_counts": {"😀": 5},
        "top_activities": [["running", 3]]
    }
    mocker.patch('requests.get', return_value=mock_response)

    mock_col1 = mocker.MagicMock()
    mock_col2 = mocker.MagicMock()
    mock_col3 = mocker.MagicMock()
    mock_col4 = mocker.MagicMock()
    mocker.patch('streamlit.columns', return_value=[mock_col1, mock_col2, mock_col3, mock_col4])

    show_stats(user_id=1)

    mock_col1.metric.assert_called_once_with("Total Entries", 10)
    mock_col2.metric.assert_called_once_with("Average Mood", "7.50")
    mock_col3.metric.assert_called_once_with("Max", 9)
    mock_col4.metric.assert_called_once_with("Min", 5)
