"""
This file contains functions for working with peak data in a database.

The functions allow for getting, creating, and searching for peaks.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKBElement
from shapely import wkb

from fastapi.encoders import jsonable_encoder

from . import models, schemas

WKB_CUSTOM_ENCODER = {WKBElement: lambda x: str(wkb.loads(str(x)))}
# WKB* objects cannot be serialized to JSON as-is,
# see https://github.com/tiangolo/fastapi/issues/2366
# If not used, FastAPI crash upon returning an invalid JSON

# TODO ? for the likes of f'POINT({peak.lat} {peak.lon})' => sanitize values ?


def _custom_encode_peak(peak: models.Peak):
    return jsonable_encoder(
        peak,
        custom_encoder=WKB_CUSTOM_ENCODER
    )


def get_peak(db: Session, peak_id: str) -> schemas.Peak:
    """
    Retrieve a peak from the database by ID.

    :param db: SQLAlchemy session object
    :param peak_id: ID of the peak to retrieve
    :return: The peak object
    """
    return _custom_encode_peak(
        db.query(models.Peak).filter(models.Peak.id == peak_id).one()
    )


def get_peak_with_search(
    db: Session, box: schemas.BoxSearch | None,
    range_search: schemas.RangeSearch | None
) -> list[schemas.Peak]:
    """
    Retrieve peaks from the database based on a search query.

    The search query can either be a box search or a range search.

    :param db: SQLAlchemy session object
    :param box: BoxSearch object
    :param range_search: RangeSearch object
    :return: A list of peaks that match the search query
    """

    if box:
        query = db.query(
            models.Peak
        ).filter(
            func.ST_Within(
                models.Peak.geom, func.ST_MakeEnvelope(
                    box.lon_min, box.lat_min, box.lon_max, box.lat_max
                )
            )
        ).all()

        return [_custom_encode_peak(q) for q in query]

    elif range_search:
        query = db.query(
            models.Peak
        ).filter(
            func.ST_DistanceSphere(
                models.Peak.geom, func.ST_MakePoint(
                    range_search.lon, range_search.lat
                )
            ) <= range_search.range_in_meters
        ).all()

        return [_custom_encode_peak(q) for q in query]


def create_peak(db: Session, peak: schemas.Peak) -> schemas.Peak:
    db_peak = models.Peak(name=peak.name, geom=f'POINT({peak.lat} {peak.lon})')
    db.add(db_peak)
    db.commit()
    db.refresh(db_peak)
    return _custom_encode_peak(db_peak)
