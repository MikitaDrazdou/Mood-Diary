import pytest

from app.streamlit_frontend.main import main


@pytest.fixture(autouse=True)
def mock_streamlit(mocker):
    mock = mocker.patch('app.streamlit_frontend.main.st')
    mock.session_state = {}
    return mock


def test_authenticated_flow(mocker, mock_streamlit):
    mock_streamlit.session_state.update({
        'user': 'test_user',
        'user_id': 123,
        'page': 'dashboard'
    })
    mock_dashboard = mocker.patch('app.streamlit_frontend.main.dashboard')

    main()
    mock_dashboard.assert_called_once()
