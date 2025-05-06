from unittest.mock import Mock

from app.streamlit_frontend.utils import get_user_id_from_login_response


def test_get_user_id_from_login_response_success():
    mock_response = Mock()
    mock_response.json.return_value = {'user_id': 123}
    assert get_user_id_from_login_response(mock_response) == 123


def test_get_user_id_from_login_response_failure():
    mock_response = Mock()
    mock_response.json.side_effect = ValueError
    assert get_user_id_from_login_response(mock_response) is None
