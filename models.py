from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class Room:
    number: int
    wing: str
    floor: int
    category: str
    bed_possible: str
    max_guests: int
    bed_mounted: Optional[str] = None
    ready: Optional[bool] = None
    status: Optional[str] = None

@dataclass
class Booking:
    booking_id: str
    category: str # "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"
    guests: int #number of guests
    has_children: bool #if there are children, has_children is True.
    has_elderly: bool #if there are elderly, has_elderly is True.
    check_in: date
    check_out: date
    notes: str


@dataclass
class HouseView:
    room_number: int
    house_status: str # "free", "booked", "occupied", "maintenance", "out of order"
    mounted: str
    notes: str
    checkout_date: Optional[date] = None



