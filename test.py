from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# TODO
# Docker broke, couldn't run any tests


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == "Welcome to Pique API."


def test_post_peak():
    pass
    # TODO


def test_read_peak():
    response = client.get('/peaks/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Mt. Everest'}


def test_search_peak_with_box_parameters():
    response = client.get(
        '/peaks/',
        params={
            'lon_min': -180,
            'lat_min': -90,
            'lon_max': 180,
            'lat_max': 90
        }
    )
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'name': 'Mt. Everest'},
        {'id': 2, 'name': 'K2'},
        {'id': 3, 'name': 'Kangchenjunga'}
    ]


def test_search_peak_with_range_parameters():
    response = client.get(
        '/peaks/',
        params={
            'range_in_meters': 20000,
            'lat': 27.988056,
            'lon': 86.925278
        }
    )
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'name': 'Mt. Everest'},
        {'id': 2, 'name': 'K2'}
    ]
