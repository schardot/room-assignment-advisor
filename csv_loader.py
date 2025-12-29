import csv
from models import Room, Booking, HouseView
from datetime import date

def load_rooms_main(path: str) -> list[Room]:
    rooms = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rooms.append(
                Room(
                    number=int(row["room_number"]),
                    wing=row["wing"],
                    floor=int(row["floor"]),
                    category=row["category"],
                    bed_possible=row["bed_possible"],
                    max_guests=int(row["max_guests"])
                )
            )
    return rooms


def load_rooms_status_today(path: str) -> list[dict]:
    rooms_status = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["room_number"]:
                rooms_status.append({
                    "room_number": int(row["room_number"]),
                    "status": row["status"],
                    "bed_mounted": row.get("bed_mounted", ""),
                    "ready": row.get("ready", "false").lower() == "true"
                })
    return rooms_status

def load_checkins_today(path: str) -> list[Booking]:
    checkins = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            checkins.append(Booking(
                booking_id=row["booking_id"],
                category=row["category"],
                guests=int(row["guests"]),
                has_children=row["has_children"].lower() == "true",
                has_elderly=row["has_elderly"].lower() == "true",
                check_in=date.fromisoformat(row["check_in"]),
                check_out=date.fromisoformat(row["check_out"]),
                notes=row["notes"],
            ))
    return checkins

def load_house_view_today(path: str) -> list[HouseView]:
    house_view = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            checkout_date_value = None
            if row["checkout_date"]:
                checkout_date_value = date.fromisoformat(row["checkout_date"])
            house_view.append(HouseView(
                room_number=int(row["room_number"]),
                house_status=row["house_status"],
                mounted=row["mounted"],
                notes=row["notes"],
                checkout_date=checkout_date_value,
            ))
    return house_view