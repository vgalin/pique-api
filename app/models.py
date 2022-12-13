from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from geoalchemy2 import Geometry
from .database import Base

# class Jargon(Base):
#     __tablename__ = "jargons"

#     id = Column(Integer, primary_key=True, index=True)
#     value = Column(String, index=True)
#     desc = Column(String)
#     type = Column(String)
#     group = Column(String)
#     added = Column(DateTime)
#     edited = Column(DateTime)

class Peak(Base):
    __tablename__ = 'peak'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    geom = Column(Geometry('POINT'))
