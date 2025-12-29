from typing import Optional
from models import Booking, HouseRoom
from .rules import (
    filter_by_category,
    prefer_ground_floor_if_no_stairs,
)


def recommend_room(
    booking: Booking,
    house_state: dict[int, HouseRoom],
) -> Optional[HouseRoom]:

    rooms = list(house_state.values())

    rooms = filter_by_category(booking, rooms)
    rooms = prefer_ground_floor_if_no_stairs(booking, rooms)

    if not rooms:
        return None

    return rooms[0]
