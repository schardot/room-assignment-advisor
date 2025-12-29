from models import Booking, HouseRoom
from llm.constraint_extractor import extract_constraints


def filter_by_category(booking: Booking, rooms: list[HouseRoom]) -> list[HouseRoom]:
    return [
        r for r in rooms
        if r.category == booking.category
        and r.max_guests >= booking.guests
        and r.usable_today
    ]


def prefer_ground_floor_if_no_stairs(
    booking: Booking,
    rooms: list[HouseRoom],
) -> list[HouseRoom]:
    if not booking.notes:
        return rooms

    constraints = extract_constraints(booking.notes)
    if constraints["no_stairs"]:
        return [r for r in rooms if r.floor == 0]
    return rooms

