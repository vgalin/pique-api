from pydantic import BaseModel


class Peak(BaseModel):
    id: int
    name: str
    geom: str
    elevation: int

    class Config:
        orm_mode = True


class PeakCreate(BaseModel):
    name: str | None = None
    lat: float
    lon: float
    elevation: int | None = None


class PeakUpdate(BaseModel):
    name: str | None = None
    lat: float | None = None
    lon: float | None = None
    elevation: int | None = None


# as-is, the following should not be the current file
class BoxSearch(BaseModel):
    lon_min: float  # xmin
    lat_min: float  # ymin
    lon_max: float  # merry xmax
    lat_max: float  # ymax


class RangeSearch(BaseModel):
    range_in_meters: int
    lat: float
    lon: float
