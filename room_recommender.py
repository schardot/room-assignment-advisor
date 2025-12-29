from typing import Optional, Dict
from models import Booking, HouseRoom

def recommend_room_by_category(
    booking: Booking,
    house_state: Dict[int, HouseRoom],
) -> Optional[HouseRoom]:
    """
    Recommend a room that matches booking category and is usable today.
    """
    for room in house_state.values():
        if not room.usable_today:
            continue
        if room.category != booking.category:
            continue
        return room
    return None