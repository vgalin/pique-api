import requests

everest = {
    'id': 1,
    'name': 'Mt. Everest',
    'lat': 27.986065,
    'lon': 86.922623,
    'elevation': 8849,
}

k2 = {
    'id': 2,
    'name': 'K2',
    'lat': 35.880981,
    'lon': 76.508102,
    'elevation': 8611,
}

kangchenjunga = {
    'id': 3,
    'name': 'Kangchenjunga',
    'lat': 27.702414,
    'lon': 88.147881,
    'elevation': 8586
}

BASE_URL = 'http://127.0.0.1'
peaks = [everest, k2, kangchenjunga]

# docker-compose down --volumes


def test_read_root():
    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200
    assert response.json() == 'Welcome to Pique API.'


def test_post_peak():
    for peak in peaks:
        response = requests.post(
            f'{BASE_URL}/peaks/',
            json=dict(
                name=peak['name'], elevation=peak['elevation'],
                lat=peak['lat'], lon=peak['lon'])
        )

        assert response.status_code == 200
        assert response.json()['id'] == peak['id']
        assert response.json()['name'] == peak['name']
        assert response.json()['geom'] == f'POINT ({peak["lat"]} {peak["lon"]})'
        assert response.json()['elevation'] == peak['elevation']


def test_read_peak():
    for peak in peaks:
        response = requests.get(f'{BASE_URL}/peaks/{peak["id"]}')
        assert response.status_code == 200
        assert response.json()['id'] == peak['id']
        assert response.json()['name'] == peak['name']
        assert response.json()['geom'] == f'POINT ({peak["lat"]} {peak["lon"]})'
        assert response.json()['elevation'] == peak['elevation']


def test_search_peak_with_box_parameters_all_peaks():
    response = requests.get(
        f'{BASE_URL}/peaks/?lon_min=-99&lat_min=-99&lon_max=99&lat_max=99'
    )
    assert response.status_code == 200
    for item, peak in zip(response.json(), peaks):
        assert item['id'] == peak['id']
        assert item['name'] == peak['name']
        assert item['geom'] == f'POINT ({peak["lat"]} {peak["lon"]})'


def test_search_peak_with_box_parameters_only_two_peaks():
    # search only Mt. Everest and Kangchenjunga (due ton 86<lon<89)
    response = requests.get(
        f'{BASE_URL}/peaks/?lon_min=86&lat_min=-99&lon_max=89&lat_max=99'
    )
    for item, peak in zip(response.json(), peaks[0] | peaks[2]):
        assert item['id'] == peak['id']
        assert item['name'] == peak['name']
        assert item['geom'] == f'POINT ({peak["lat"]} {peak["lon"]})'
        assert item['elevation'] == peak['elevation']


def test_search_peak_with_range_parameters_all_peaks():
    response = requests.get(
        f'{BASE_URL}/peaks/?lon=0&lat=0&range_in_meters=99999999'
    )
    assert response.status_code == 200
    for item, peak in zip(response.json(), peaks):
        assert item['id'] == peak['id']
        assert item['name'] == peak['name']
        assert item['geom'] == f'POINT ({peak["lat"]} {peak["lon"]})'
        assert item['elevation'] == peak['elevation']


# TODO more advanced searches


def test_update_name():
    peak = peaks[0]
    response = requests.put(
        f'{BASE_URL}/peaks/{peak["id"]}',
        json=dict(
            name=peak['name'] + '-UPD', elevation=peak['elevation'],
            lat=peak['lat'], lon=peak['lon'],
        )
    )
    assert response.status_code == 200
    assert response.json()['name'] == peak['name'] + '-UPD'


# TODO more advanced updates


def test_delete_all():
    for peak in peaks:
        response = requests.delete(
            f'{BASE_URL}/peaks/{peak["id"]}',
        )
        assert response.status_code == 200
        assert response.json()['id'] == peak['id']

    assert requests.get(
        f'{BASE_URL}/peaks/?lon=0&lat=0&range_in_meters=99999999'
    ).json() == []
