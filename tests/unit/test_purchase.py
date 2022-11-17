import pytest

import server

@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def club():
    one_club = server.clubs[0]
    one_club["points"] = 4
    return one_club['name']

@pytest.fixture
def competition():
    return server.competitions[0]['name']

class TestPurchase:
    def test_purchase_too_many_places(self, client, club, competition):
        """Checks response when authenticated user request"""
        response = client.post(
            "/purchasePlaces",
            data={'places':8, 'club':club, 'competition':competition},
            follow_redirects=True
            )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("You did not have enought points") != -1
        assert data.find("Great-booking complete!") != -1

    def test_purchase_legal_number_places(self, client, club, competition):
        """Checks response when authenticated user request"""
        response = client.post(
            "/purchasePlaces",
            data={'places':4, 'club':club, 'competition':competition},
            follow_redirects=True
            )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Great-booking complete!") != -1
        assert data.find("You did not have enought points") == -1
