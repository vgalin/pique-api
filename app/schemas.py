from pydantic import BaseModel


class PeakCreate(BaseModel):
    name: str | None
    lat: float
    lon: float


class Peak(BaseModel):
    id: int
    name: str
    # lat: float
    # lon: float
    geom: str
    # TODO 'elevation' attribute would be nice

    class Config:
        orm_mode = True


class PeakUpdate(BaseModel):
    name: str | None = None
    lat: float | None = None
    lon: float | None = None


# as-is, the following should not be in this peculiar file
class BoxSearch(BaseModel):
    lon_min: float  # xmin
    lat_min: float  # ymin
    lon_max: float  # merry xmax
    lat_max: float  # ymax


class RangeSearch(BaseModel):
    range_in_meters: int
    lat: float
    lon: float
