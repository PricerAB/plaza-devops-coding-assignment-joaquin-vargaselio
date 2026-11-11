from fastapi.testclient import TestClient
from webapp.src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_star_wars_data_default():
    response = client.get("/data")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "height" in data
    assert "mass" in data

def test_get_star_wars_data_with_custom_id():
    response = client.get("/data?id=3")
    assert response.status_code == 200
    data = response.json()
    assert data.get("name") == "R2-D2"

def test_get_star_wars_data_not_found():
    response = client.get("/data?id=99999")
    assert response.status_code in [404, 500]

def test_get_top_people_by_bmi():
    response = client.get("/top-people-by-bmi")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) <= 20
    
    if len(data) > 0:
        assert "bmi" in data[0]
        if len(data) > 1:
            assert data[0]["bmi"] >= data[1]["bmi"]