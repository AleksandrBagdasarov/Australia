from sqlalchemy import Column, String, Integer, Float, Text
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


class InvestorMetrics(Base):
    __tablename__ = 'investor_metrics'
    saburb = Column(Integer)
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_types = Column(String(64), nullable=False)
    bedrooms = Column(String(64), nullable=False)
    median_sold_price = Column(Integer, nullable=True)
    median_sold_price_five_years_ago = Column(Integer, nullable=True)
    median_rental_price = Column(Integer, nullable=True)
    rental_yield = Column(Float, nullable=True)
    annual_growth = Column(Float, nullable=True)
    rental_demand = Column(Float, nullable=True)
    rental_properties = Column(Integer, nullable=True)
    sold_properties = Column(Integer, nullable=True)
    sold_properties_five_years_ago = Column(Integer, nullable=True)
    polygon = Column(Text)
    metro = Column(String(64), nullable=False)


class InvestorMetricsExceptions(Base):
    __tablename__ = 'investor_metrics_exceptions'
    saburb = Column(Integer)
    suburb_url = Column(String(1024), nullable=False)
