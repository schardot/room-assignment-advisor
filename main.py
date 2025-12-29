from house_state import build_house_state
from csv_loader import load_checkins_today
from room_recommender.recommender import recommend_room

house_state = build_house_state(
    "data/rooms_main.csv",
    "data/rooms_status_today.csv",
    "data/house_view_today.csv",
)

checkins = load_checkins_today("data/checkins_today.csv")

booking = checkins[0]

room = recommend_room(booking, house_state)

print(f"Booking {booking.booking_id}")

if room:
    print(f"Recommended room: {room.number} (category {room.category})")
else:
    print("No suitable room found")
