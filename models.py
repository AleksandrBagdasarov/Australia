from sqlalchemy import Column, String, Integer, Float, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class Suburbs(Base):
    __tablename__ = 'Suburbs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    suburb_url = Column(String(1024), nullable=False)
    suburb = Column(String(64))
    state = Column(String(64))
    postcode = Column(String(64))


class InvestorMetrics(Base):
    __tablename__ = 'Investor_metrics'
    saburb_id = Column(Integer)
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
    metro = Column(String(64), nullable=True)


class Polygons(Base):
    __tablename__ = 'Polygons'
    saburb_id = Column(Integer)
    polygon = Column(Text)


class PropertyLinks(Base):
    __tablename__ = 'Property_links'
    saburb_id = Column(Integer, primary_key=True)
    url_buy = Column(String(1024), nullable=True)
    url_rent = Column(String(1024), nullable=True)
    url_sold = Column(String(1024), nullable=True)


class Visits_per_property_in_suburb(Base):
    __tablename__ = 'Visits_per_property_in_suburb'
    saburb_id = Column(Integer)
    url_api = Column(String(1024), nullable=True)
    visits_per_property_of_suburb = Column(Integer, nullable=True)
    average_of_State = Column(Integer, nullable=True)


class SoldPropertyData(Base):
    __tablename__ = 'Sold_property_data'
    suburb_id = Column(Integer)
    agent_name = Column(String(256), nullable=True)
    agent_pic_url = Column(String(1024), nullable=True)
    agency_name = Column(String(256), nullable=True)
    agency_logo_url = Column(String(1024), nullable=True)
    price = Column(String(256), nullable=True)
    address = Column(String(256), nullable=True)
    number_of_bedrooms = Column(Integer, nullable=True)
    number_of_bathrooms = Column(Integer, nullable=True)
    number_of_car_spaces = Column(Integer, nullable=True)
    sold_date = Column(Date, nullable=True)
    url_to_listing = Column(String(1024), nullable=True, unique=True)
    url_of_default_hero_image = Column(String(1024), nullable=True)

    construction_status = Column(String(256), nullable=True)
    property_type = Column(String(256), nullable=True)
    property_type_group = Column(String(256), nullable=True)
    agency_web_site = Column(String(256), nullable=True)