from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from geoalchemy2.elements import WKBElement
from shapely import wkb

from .database import SessionLocal, engine
from . import crud, models, schemas, config


# TODO mention WGS84 somewhere? (if it is indeed the system used)


models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=config.DEBUG)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# WKB* objects must be encoded to be to JSON-serializable
def encode_peak(peak: models.Peak):
    return jsonable_encoder(
        peak,
        custom_encoder={WKBElement: lambda x: str(wkb.loads(str(x)))}
    )


@app.get('/')
def read_root():
    return "Welcome to Pique API."


@app.get('/peaks/{peak_id}', response_model=schemas.Peak)
def read_peak(
    peak_id: int,
    db: Session = Depends(get_db),
):
    db_peak = crud.get_peak(db=db, peak_id=peak_id)
    if not db_peak:
        raise HTTPException(
            status_code=404,
            detail='Peak with given id not found.'
        )
    return encode_peak(db_peak)


@app.get('/peaks/', response_model=schemas.Peak | list[schemas.Peak])
def search_peak(
    lon_min: float | None = None,  # xmin
    lat_min: float | None = None,  # ymin
    lon_max: float | None = None,  # xmax
    lat_max: float | None = None,  # ymax

    range_in_meters: int | None = None,
    lat: float | None = None,
    lon: float | None = None,

    db: Session = Depends(get_db),
):
    # TODO, cleaner way for many parameters?

    box = None
    range_search = None

    box_params = (lon_min, lat_min, lon_max, lat_max)
    range_params = (range_in_meters, lat, lon)

    if any(box_params) and any(range_params):
        raise HTTPException(
            status_code=400,
            detail='Box Search and Range Search cannot be used together.'
        )

    if None not in box_params:
        box = schemas.BoxSearch(
            lon_min=lon_min, lat_min=lat_min,
            lon_max=lon_max, lat_max=lat_max
        )

    if None not in range_params:
        range_search = schemas.RangeSearch(
            range_in_meters=range_in_meters,
            lat=lat, lon=lon
        )

    if not (box or range_search):
        raise HTTPException(
            status_code=400,
            detail='Missing query parameters for Box Search or Range Search.'
        )

    search_results = crud.get_peak_with_search(
        db=db, box=box, range_search=range_search
    )
    return [encode_peak(result) for result in search_results]


@app.post('/peaks/', response_model=schemas.Peak)
def create_peak(peak: schemas.PeakCreate, db: Session = Depends(get_db)):
    return encode_peak(
        crud.create_peak(db=db, peak=peak)
    )


@app.put('/peaks/{peak_id}', response_model=schemas.Peak)
def update_peak(
    peak_id: int,
    peak_update: schemas.PeakUpdate,
    db: Session = Depends(get_db)
):
    db_peak = crud.get_peak(db=db, peak_id=peak_id)
    if not db_peak:
        raise HTTPException(
            status_code=404,
            detail='Peak with given id not found.'
        )
    return encode_peak(
        crud.update_peak(db=db, db_peak=db_peak, peak_update=peak_update)
    )


@app.delete('/peaks/{peak_id}', response_model=schemas.Peak)
def delete_peak(peak_id: int, db: Session = Depends(get_db)):
    db_peak = crud.get_peak(db=db, peak_id=peak_id)
    if not db_peak:
        raise HTTPException(
            status_code=404,
            detail='Peak with given id not found.'
        )
    crud.delete_peak(db, peak_id)
    return encode_peak(
        db_peak
    )
