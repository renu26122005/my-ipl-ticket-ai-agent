from google.adk.agents import Agent
import random
import datetime

# Mock IPL 2026 data
TEAMS = ["CSK", "MI", "RCB", "KKR", "SRH", "DC", "PBKS", "GT", "LSG", "RR"]
STADIUMS = ["Wankhede Mumbai", "Chepauk Chennai", "Chinnaswamy Bangalore", "Eden Gardens Kolkata"]
CATEGORIES = ["General", "Silver", "Gold", "Platinum"]

matches_data = {}
bookings_data = {}

def _generate_mock_matches():
    global matches_data
    if matches_data:
        return
    
    start_date = datetime.date(2026, 3, 22)
    for i in range(1, 11):
        match_id = f"IPL2026_M{i}"
        team1, team2 = random.sample(TEAMS, 2)
        stadium = random.choice(STADIUMS)
        match_date = start_date + datetime.timedelta(days=i-1)
        total_seats = random.randint(30000, 50000)
        available_seats = random.randint(1000, total_seats)
        
        matches_data[match_id] = {
            "match_id": match_id,
            "teams": f"{team1} vs {team2}",
            "date": match_date.strftime("%Y-%m-%d"),
            "stadium": stadium,
            "total_seats": total_seats,
            "available_seats": available_seats
        }

_generate_mock_matches()

def get_matches() -> list[dict]:
    """
    Returns a list of upcoming IPL matches with match_id, teams, date, stadium, total_seats, and available_seats.
    """
    return list(matches_data.values())

def check_seats(match_id: str) -> dict:
    """
    Returns seat availability, price range (₹500–₹5000), and categories (General, Silver, Gold, Platinum) for a given match_id.
    """
    if match_id not in matches_data:
        return {"error": "Match not found. Please provide a valid match_id."}
    
    match = matches_data[match_id]
    
    return {
        "match_id": match_id,
        "available_seats": match["available_seats"],
        "price_range": "₹500 - ₹5000",
        "categories": CATEGORIES
    }

def book_ticket(match_id: str, name: str, seats: int, category: str) -> dict:
    """
    Simulates booking tickets for an IPL match. Generates a booking_id, confirms the booking, and updates the seat count.
    """
    if match_id not in matches_data:
        return {"error": "Match not found. Please provide a valid match_id."}
    
    if category not in CATEGORIES:
        return {"error": f"Invalid category. Choose from: {', '.join(CATEGORIES)}"}
    
    if seats <= 0:
        return {"error": "Number of seats must be greater than 0."}
    
    match = matches_data[match_id]
    if match["available_seats"] < seats:
        return {"error": f"Not enough seats available. Only {match['available_seats']} seats left."}
    
    # Update seat count
    match["available_seats"] -= seats
    
    # Generate booking ID
    booking_id = f"BKG_{random.randint(10000, 99999)}_{match_id}"
    
    # Store booking
    bookings_data[booking_id] = {
        "booking_id": booking_id,
        "match_id": match_id,
        "name": name,
        "seats": seats,
        "category": category,
        "status": "CONFIRMED",
        "booking_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return {
        "status": "Success",
        "message": "Tickets booked successfully!",
        "booking_id": booking_id,
        "booking_details": bookings_data[booking_id]
    }

def get_booking_status(booking_id: str) -> dict:
    """
    Returns booking details and status for a given booking_id.
    """
    if booking_id not in bookings_data:
        return {"error": "Booking not found. Please provide a valid booking_id."}
    
    return bookings_data[booking_id]

# Create the root agent
root_agent = Agent(
    name="ipl_ticket_booking_agent",
    model="gemini-flash-latest",
    description="IPL ticket booking assistant AI agent",
    instruction=(
        "Act as a friendly IPL assistant that helps users view matches, check seats, book tickets, "
        "and confirm bookings step-by-step. Always use tools to fetch data and process bookings, "
        "and never hallucinate data."
    ),
    tools=[get_matches, check_seats, book_ticket, get_booking_status]
)
