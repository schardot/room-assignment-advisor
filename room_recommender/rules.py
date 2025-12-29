from models import Booking, HouseRoom


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

    notes = booking.notes.lower()
    if "no stairs" not in notes and "sem escadas" not in notes:
        return rooms

    ground = [r for r in rooms if r.floor == 0]
    return ground if ground else rooms
