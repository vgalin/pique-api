"""
This file contains functions for working with peak data in a database.

The functions allow for getting, creating, and searching for peaks.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas


# TODO ? for the likes of f'POINT({peak.lat} {peak.lon})' => sanitize values ?


def get_peak(db: Session, peak_id: int) -> schemas.Peak | None:
    """
    Retrieve a peak from the database by ID.

    :param db: SQLAlchemy session object
    :param peak_id: ID of the peak to retrieve
    :return: The peak object
    """
    return db.query(models.Peak).filter(models.Peak.id == peak_id).first()


def get_peak_with_search(
    db: Session,
    box: schemas.BoxSearch | None,
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

        return [q for q in query]

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

        return [q for q in query]


def create_peak(db: Session, peak: schemas.Peak) -> schemas.Peak:
    """
    Insert a peak in the database.

    :param db: SQLAlchemy session object
    :return: The created peak
    """
    db_peak = models.Peak(name=peak.name, geom=f'POINT({peak.lat} {peak.lon})')
    db.add(db_peak)
    db.commit()
    db.refresh(db_peak)
    return db_peak


def update_peak(
    db: Session,
    db_peak: schemas.Peak,
    peak_update: schemas.PeakUpdate
) -> schemas.Peak:
    """
    Update a peak in the database.

    :param db_peak: A Peak schema
    :param db: SQLAlchemy session object
    :return: The updated peak
    """
    db_peak.name = peak_update.name
    db_peak.geom = f'POINT({peak_update.lat} {peak_update.lon})'

    db.commit()
    db.refresh(db_peak)
    return db_peak


def delete_peak(db: Session, peak_id: int):
    """
    Delete a peak in the database.

    :param peak_id: A Peak schema
    :param db: SQLAlchemy session object
    """
    db_peak = get_peak(db, peak_id)
    db.delete(db_peak)
    db.commit()
