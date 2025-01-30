from pydantic import BaseModel
from datetime import datetime

class BikeRegistration(BaseModel):
    serial_number: str


class TokenRegistration(BaseModel):
    name: str
    symbol: str
    address: str


class TripRegistration(BaseModel):
    user_id: int
    bike_id: int
    travelled_distance: float
    source_parking_station_id: int 
    destination_parking_station_id: int 
    source_timestamp: datetime
    destination_timestamp: datetime


class UserRegistration(BaseModel):
    name: str
    address: str