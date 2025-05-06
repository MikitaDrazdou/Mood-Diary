import pytest


@pytest.fixture
def mock_requests(mocker):
    return mocker.patch('requests.post')


@pytest.fixture
def mock_post(mocker):
    return mocker.patch('requests.post')
