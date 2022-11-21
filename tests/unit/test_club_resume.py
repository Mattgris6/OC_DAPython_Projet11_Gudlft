import pytest

import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

class TestClubs:
    def test_display_clubs_resume(self, client):
        """Checks response when get display page"""
        response = client.get('/clubResume')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Liste des clubs") != -1
