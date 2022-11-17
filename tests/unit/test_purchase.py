import pytest

import server

@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def club():
    return server.clubs[0]

@pytest.fixture
def competition():
    return server.competitions[0]

class TestPurchase:
    def test_purchase_too_many_places(self, client, club, competition):
        club["points"] = 4
        competition["numberOfPlaces"] = 25
        response = client.post(
            "/purchasePlaces",
            data={'places':8, 'club':club["name"], 'competition':competition["name"]},
            follow_redirects=True
            )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("You do not have enough points") != -1
        assert data.find("How many places") != -1

    def test_purchase_legal_number_places(self, client, club, competition):
        club["points"] = 4
        competition["numberOfPlaces"] = 25
        response = client.post(
            "/purchasePlaces",
            data={'places':4, 'club':club["name"], 'competition':competition["name"]},
            follow_redirects=True
            )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Great-booking complete!") != -1

    def test_purchase_more_than_max_places_in_one_time(self, client, club, competition):
        club["points"] = 20
        competition["numberOfPlaces"] = 25
        response = client.post(
            "/purchasePlaces",
            data={'places':14, 'club':club["name"], 'competition':competition["name"]},
            follow_redirects=True
            )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("You can not purchase more than 12 places per competition") != -1
        assert data.find("How many places?") != -1
    
    def test_purchase_more_than_max_places_in_multiple_times(self, client, club, competition):
        club["points"] = 20
        competition["numberOfPlaces"] = 25
        response = client.post(
            "/purchasePlaces",
            data={'places':7, 'club':club["name"], 'competition':competition["name"]},
            follow_redirects=True
            )
        response = client.post(
            "/purchasePlaces",
            data={'places':7, 'club':club["name"], 'competition':competition["name"]},
            follow_redirects=True
            )
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("You can not purchase more than 12 places per competition") != -1
        assert data.find("How many places?") != -1
