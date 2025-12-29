from csv_loader import (
    load_rooms_main,
    load_rooms_status_today,
    load_checkins_today,
    load_house_view_today,
)

print("Rooms:", len(load_rooms_main("data/rooms_main.csv")))
print("Room statuses:", len(load_rooms_status_today("data/rooms_status_today.csv")))
print("Check-ins:", len(load_checkins_today("data/checkins_today.csv")))
print("House view entries:", len(load_house_view_today("data/house_view_today.csv")))
