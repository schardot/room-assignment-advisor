from typing import Dict
from models import HouseRoom, Room
from csv_loader import load_rooms_main, load_rooms_status_today, load_checkins_today, load_house_view_today

def build_house_state(
    rooms_main_path: str,
    rooms_status_path: str,
    house_view_path: str,
) -> Dict[int, HouseRoom]:
    """
    Merge multiple CSV sources into a unified house state.
    """

    rooms_main = load_rooms_main(rooms_main_path)
    rooms_status = load_rooms_status_today(rooms_status_path)
    house_view = load_house_view_today(house_view_path)

    status_by_room = {r["room_number"]: r for r in rooms_status}
    house_view_by_room = {r.room_number: r for r in house_view}

    house_state = {}

    for room in rooms_main:
        room_number = room.number

        status = status_by_room.get(room_number, {})
        view = house_view_by_room.get(room_number)

        effective_status = status.get("status", "unknown")
        ready = status.get("ready", False)

        house_status = view.house_status if view else None
        usable_today = (effective_status == "free") or (house_status == "free")

        house_state[room_number] = HouseRoom(
            number=room_number,
            wing=room.wing,
            floor=room.floor,
            category=room.category,
            bed_possible=room.bed_possible,
            max_guests=room.max_guests,
            status=effective_status,
            bed_mounted=view.mounted if view else "unknown",
            ready=ready,
            usable_today=usable_today,
        )
    return house_state