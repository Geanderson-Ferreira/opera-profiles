from sqlalchemy import (
    create_engine, Column, String, Integer, Boolean,
    Text, ForeignKey, DateTime, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from os import environ
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'
    hotel_id = Column(String(10), primary_key=True)
    hotel_name = Column(String(255))
    rules = relationship("HotelRule", back_populates="hotel")

    def __repr__(self):
        return f"<Hotel(hotel_id='{self.hotel_id}', hotel_name='{self.hotel_name}')>"

class Rule(Base):
    __tablename__ = 'rules'
    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    rule_description = Column(String(255))
    rule_code = Column(Text)
    rule_type = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    hotels = relationship("HotelRule", back_populates="rule")

    def __repr__(self):
        return f"<Rule(rule_id={self.rule_id}, rule_description='{self.rule_description}', is_active={self.is_active})>"

class HotelRule(Base):
    __tablename__ = 'hotel_rules'
    hotel_id = Column(String(10), ForeignKey('hotels.hotel_id'), primary_key=True)
    rule_id = Column(Integer, ForeignKey('rules.rule_id'), primary_key=True)
    hotel = relationship("Hotel", back_populates="rules")
    rule = relationship("Rule", back_populates="hotels")
    def __repr__(self):
        return f"<HotelRule(hotel_id='{self.hotel_id}', rule_id={self.rule_id})>"

def connect_and_create_tables(database_url):

    engine = create_engine(database_url, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session, engine