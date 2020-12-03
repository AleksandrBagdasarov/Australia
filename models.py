from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class Suburbs(Base):
    __tablename__ = 'suburb'
    id = Column(Integer, primary_key=True, autoincrement=True)
    suburb_url = Column(String(1024), nullable=False)
    suburb = Column(String(64))
    state = Column(String(64))
    postcode = Column(String(64))
    # suburbs_stats = relationship('suburbs_stats', uselist=False, back_populates='suburb')


class Suburbs_exception(Base):
    __tablename__ = 'suburbs_exception'
    id = Column(Integer, primary_key=True, autoincrement=True)
    suburb_url = Column(String(1024), nullable=False)


class SuburbsStats(Base):
    __tablename__ = 'suburbs_stats'
    # saburb = relationship('suburb', back_populates='suburbs_stats')
    id = Column(Integer, primary_key=True, autoincrement=True)
    properties_available_for_rent = Column(Integer, nullable=True)
    properties_available_for_sale = Column(Integer, nullable=True)
    median_property_price_for_houses = Column(Integer, nullable=True)
    median_property_prices_for_units = Column(Integer, nullable=True)
    average_house_rent_per_week = Column(Integer, nullable=True)
    average_house_rent_yield = Column(Integer, nullable=True)
    average_unit_rent_per_week = Column(Integer, nullable=True)
    average_unit_rent_yield = Column(Integer, nullable=True)
    five_year_house_growth_rate = Column(Integer, nullable=True)
    five_year_unit_growth_rate = Column(Integer, nullable=True)
