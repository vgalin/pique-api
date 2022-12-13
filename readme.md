<p align="center">
<img align="center"  width="200" src="logo-pique.png">
</p>

<h1 align="center"> Pique API </h1>


**Pique API** is a FastAPI-based web service for accessing and managing `Mountain Peaks`. It uses a PostGIS-enabled PostgreSQL database for storage and querying.

## Prerequisites
- Docker

## Installation

Clone this repository:
```shell
git clone https://github.com/vgalin/pique-api.git
```

CD into the cloned directory and run a docker-compose build:
```shell
cd pique-api
docker-compose build
```

Start the Docker containers:
```shell
docker-compose up
```
The API will then be available at `http://localhost:80`.
## Usage
### Endpoints

- `GET /`: Welcome message
- `GET /peaks/{peak_id}`: Retrieve peak with specified ID.
- `GET /peaks/`: Search for peaks within a specified box or range.
- `POST /peaks/`: Create a new peak.

### Query parameters

The `/peaks/` endpoint supports the following query parameters for searching peaks within a box:

- `lon_min`: The minimum longitude of the box.
- `lat_min`: The minimum latitude of the box.
- `lon_max`: The maximum longitude of the box.
- `lat_max`: The maximum latitude of the box.

Alternatively, the following query parameters can be used to search for peaks within a specified range:

- `range_in_meters`: The range to search within, in meters.
- `lat`: The latitude of the center of the range.
- `lon`: The longitude of the center of the range.

## Known issues
- After `docker-compose up`, the API cannot reach the DB. Workaround: CTRL-C / SIGINT docker compose and re run it.

## License

This project is licensed under the MIT License.