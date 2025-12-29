# Room Assignment Advisor

An intelligent room recommendation system that matches hotel bookings with available rooms based on category, capacity, availability, and accessibility constraints extracted from booking notes.

## Overview

The Room Assignment Advisor processes daily check-ins and recommends suitable rooms by:

- Matching booking categories and guest capacity requirements
- Checking real-time room availability from multiple data sources
- Extracting accessibility constraints from booking notes using LLM or keyword matching
- Applying filtering rules to find the best room match

## Features

- **Multi-source room data integration**: Combines room master data, daily status, and house view
- **Intelligent constraint extraction**: Uses local LLM (Ollama) or keyword matching to understand booking requirements
- **Smart availability detection**: Considers both status reports and operational house view
- **Accessibility-aware recommendations**: Automatically filters for ground floor when stairs are not accessible

## Project Structure

```
room-assignment-advisor/
├── data/                          # CSV data files
│   ├── rooms_main.csv            # Master room data (categories, capacity, etc.)
│   ├── rooms_status_today.csv    # Daily room status
│   ├── house_view_today.csv       # Operational house view
│   └── checkins_today.csv        # Today's check-ins
├── llm/
│   └── constraint_extractor.py  # LLM-based constraint extraction
├── room_recommender/
│   ├── recommender.py            # Main recommendation logic
│   └── rules.py                  # Filtering rules
├── csv_loader.py                  # CSV data loading utilities
├── house_state.py                 # House state builder
├── models.py                      # Data models
└── main.py                        # Entry point

```

## Installation

### Prerequisites

- Python 3.10+
- (Optional) Ollama for LLM-based constraint extraction

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd room-assignment-advisor
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install langchain-core langchain-ollama
```

Or for fallback support:

```bash
pip install langchain-core langchain-community
```

**Note**: The system works without LLM packages - it will automatically fall back to keyword matching.

### Optional: Setup Ollama for LLM Features

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Pull a model:

```bash
ollama pull llama3
```

The system will automatically detect and use Ollama if available.

## Usage

### Basic Usage

```python
from house_state import build_house_state
from csv_loader import load_checkins_today
from room_recommender.recommender import recommend_room

# Build house state from CSV files
house_state = build_house_state(
    "data/rooms_main.csv",
    "data/rooms_status_today.csv",
    "data/house_view_today.csv",
)

# Load today's check-ins
checkins = load_checkins_today("data/checkins_today.csv")

# Recommend room for first booking
booking = checkins[0]
room = recommend_room(booking, house_state)

if room:
    print(f"Recommended room: {room.number} (category {room.category})")
else:
    print("No suitable room found")
```

### Running the Example

```bash
python main.py
```

## Data Format

### rooms_main.csv

Master room data with permanent attributes:

```csv
room_number,wing,floor,category,bed_possible,max_guests
201,A,0,S2,Twin/Double,3
202,A,0,S2,Twin/Double,3
```

### rooms_status_today.csv

Daily room status:
```csv
room_number,status,bed_mounted,ready
201,occupied,Double,false
202,occupied,Double,false
203,free,Twin,false
```

**Status values**: `free`, `occupied`, `maintenance`

### house_view_today.csv

Operational house view (takes precedence for availability):
```csv
room_number,house_status,checkout_date,mounted,notes
201,busy,2026-01-01,Double,Checkout today
202,free,2026-01-02,Double,Ready for immediate check-in
```

**House status values**: `free`, `busy`, `blocked`

### checkins_today.csv

Today's check-in bookings:

```csv
booking_id,guest_name,guests,has_children,has_elderly,check_in,check_out,category,notes
B001,Natalia Leite,2,true,false,2026-01-01,2026-01-02,S2,"No stairs please"
```

## How It Works

### 1. House State Building

`build_house_state()` merges data from three sources:

- **rooms_main**: Base room attributes (number, wing, floor, category, capacity)
- **rooms_status_today**: Current status and readiness
- **house_view_today**: Operational availability (takes precedence)

A room is considered `usable_today` if either:

- `rooms_status_today` shows status as "free", OR
- `house_view_today` shows house_status as "free"

### 2. Constraint Extraction

`extract_constraints()` analyzes booking notes to identify requirements:

- **With LLM**: Uses Ollama (llama3) to extract structured constraints
- **Fallback**: Uses keyword matching for common phrases

Currently extracts:

- `no_stairs`: Boolean indicating if guest needs ground floor

### 3. Room Filtering

The recommendation process applies filters in sequence:

1. **Category & Capacity Filter** (`filter_by_category`):
   - Matches booking category
   - Ensures room capacity >= number of guests
   - Only includes rooms with `usable_today = True`

2. **Accessibility Filter** (`prefer_ground_floor_if_no_stairs`):
   - If constraints indicate "no_stairs", filters to ground floor (floor == 0)
   - Otherwise returns all filtered rooms

3. **Selection**: Returns the first matching room

## API Reference

### Models

#### `Booking`

```python
@dataclass
class Booking:
    booking_id: str
    category: str  # S1-S9
    guests: int
    has_children: bool
    has_elderly: bool
    check_in: date
    check_out: date
    notes: str
```

#### `HouseRoom`

```python
@dataclass
class HouseRoom:
    number: int
    wing: str
    floor: int
    category: str
    bed_possible: str
    max_guests: int
    status: str
    bed_mounted: str
    ready: bool
    usable_today: bool
```

### Functions

#### `build_house_state(rooms_main_path, rooms_status_path, house_view_path) -> Dict[int, HouseRoom]`

Merges multiple CSV sources into a unified house state dictionary.

#### `recommend_room(booking: Booking, house_state: Dict[int, HouseRoom]) -> Optional[HouseRoom]`

Recommends a suitable room for the given booking.

#### `extract_constraints(notes: str) -> Dict[str, bool]`

Extracts constraints from booking notes. Returns `{"no_stairs": bool}`.

## Extending the System

### Adding New Constraints

To extract additional constraints:

1. Update the LLM prompt in `llm/constraint_extractor.py`:

```python
template="""
...
Return ONLY a JSON object with this structure:
{{
  "no_stairs": boolean,
  "quiet_room": boolean,
  "near_parking": boolean
}}
...
"""
```

2. Update the keyword fallback list

3. Add filtering rules in `room_recommender/rules.py`

### Adding New Filtering Rules

Add new rule functions in `room_recommender/rules.py` and chain them in `recommend_room()`:

```python
def prefer_quiet_room(booking: Booking, rooms: list[HouseRoom]) -> list[HouseRoom]:
    constraints = extract_constraints(booking.notes)
    if constraints.get("quiet_room"):
        # Filter logic here
        pass
    return rooms
```

## Troubleshooting

### LLM Not Working

- Ensure Ollama is installed and running: `ollama list`
- Check model is available: `ollama pull llama3`
- System will automatically fall back to keyword matching

### No Rooms Found
- Check room availability in `house_view_today.csv`
- Verify category matches between booking and rooms
- Ensure room capacity is sufficient for number of guests

### Import Errors
- Install missing packages: `pip install langchain-core langchain-ollama`
- Or use fallback: `pip install langchain-core langchain-community`
- System works without LLM packages (uses keyword matching)

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

