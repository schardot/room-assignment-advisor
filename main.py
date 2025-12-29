from house_state import build_house_state

house_state = build_house_state(
    "data/rooms_main.csv",
    "data/rooms_status_today.csv",
    "data/house_view_today.csv",
)

total = len(house_state)
usable = sum(1 for r in house_state.values() if r.usable_today)
occupied = sum(1 for r in house_state.values() if r.status == "occupied")
blocked = sum(1 for r in house_state.values() if r.status in ("maintenance", "blocked"))

print(f"Total rooms: {total}")
print(f"Usable today: {usable}")
print(f"Occupied today: {occupied}")
print(f"Blocked today: {blocked}")
