import os
from dotenv import load_dotenv
load_dotenv()

from typing import Optional, Dict, Any, List
from pymongo import MongoClient
from datetime import datetime

from langchain.agents import create_agent

# -------------------------
# DB SETUP
# -------------------------
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["healthcare_ai"]

patients_col = db.patients
appointments_col = db.appointments

# -------------------------
# HELPERS
# -------------------------
def generate_slots():
    """Hardcoded slots (as required in task)"""
    return [
        "2026-06-21 10:00",
        "2026-06-21 11:00",
        "2026-06-21 12:00",
        "2026-06-21 14:00",
    ]

# -------------------------
# TOOLS (TASK REQUIRED)
# -------------------------

def identify_user(phone: str, name: Optional[str] = None):
    """Identify or create patient using phone number"""
    user = patients_col.find_one({"phone": phone})

    if user:
        return f"Welcome back {user.get('name', 'patient')}"

    patients_col.insert_one({
        "phone": phone,
        "name": name or "Unknown",
        "created_at": str(datetime.now())
    })

    return "New patient registered"


def fetch_slots():
    """Return available appointment slots"""
    return generate_slots()


def book_appointment(phone: str, datetime_slot: str):
    """Book appointment if slot is free"""

    existing = appointments_col.find_one({
        "datetime": datetime_slot
    })

    if existing:
        return "Slot already booked, please choose another"

    appointments_col.insert_one({
        "phone": phone,
        "datetime": datetime_slot,
        "created_at": str(datetime.now())
    })

    return f"Appointment confirmed for {datetime_slot}"


def retrieve_appointments(phone: str):
    """Get all appointments for patient"""

    docs = list(appointments_col.find({"phone": phone}))
    if not docs:
        return "No appointments found"

    return [str(d["datetime"]) for d in docs]


def cancel_appointment(phone: str, datetime_slot: str):
    """Cancel appointment"""

    res = appointments_col.delete_one({
        "phone": phone,
        "datetime": datetime_slot
    })

    if res.deleted_count == 0:
        return "No matching appointment found"

    return "Appointment cancelled"


def modify_appointment(phone: str, old_slot: str, new_slot: str):
    """Modify appointment"""

    existing = appointments_col.find_one({"datetime": new_slot})
    if existing:
        return "New slot is already booked"

    res = appointments_col.update_one(
        {"phone": phone, "datetime": old_slot},
        {"$set": {"datetime": new_slot}}
    )

    if res.matched_count == 0:
        return "Original appointment not found"

    return f"Appointment moved to {new_slot}"


def end_conversation(summary: str):
    """End conversation and return summary"""
    return f"Conversation ended. Summary: {summary}"


# -------------------------
# AGENT
# -------------------------

agent = create_agent(
    model=os.getenv("AGENT_MODEL", "openai:gpt-4o-mini"),
    tools=[
        identify_user,
        fetch_slots,
        book_appointment,
        retrieve_appointments,
        cancel_appointment,
        modify_appointment,
        end_conversation,
    ],
    system_prompt=(
        "You are a healthcare front desk voice assistant."
        "Your Responsibilities are to help patients with the following"
        "- Identify patient using phone number, and optionally name, if not found, register them"
        "- Help book, modify, cancel appointments"
        "- Always confirm date and time clearly"
        "- Keep responses short and natural"
        "- Ask for missing details"
        "Never assume patient data."
    ),
)