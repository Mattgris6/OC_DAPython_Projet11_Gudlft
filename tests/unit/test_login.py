import pytest

import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def club():
    return server.clubs[0]

class TestLogin:
    def test_should_status_code_ok(self, client):
        """Checks response when get index page"""
        response = client.get('/')
        assert response.status_code == 200

    def test_mail_correct(self, client, club):
        """Checks response when authenticated user request"""
        response = client.post("/showSummary", data={'email':club['email']}, follow_redirects=True)
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Welcome") != -1

    @pytest.mark.parametrize(
        "email, status_code",
        [
            ("", 200),
            ("aaa@bbb.co", 200),
            ("123", 200),
        ],
    )
    def test_mail_error(self, client, email, status_code):
        """Checks response when unauthenticated user request"""
        response = client.post("/showSummary", data={'email':email}, follow_redirects=True)
        assert response.status_code == status_code
        data = response.data.decode()
        assert data.find("Sorry, that email was not found.") != -1
