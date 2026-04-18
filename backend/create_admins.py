"""
Run this script once to create all admin accounts in the database.
Usage: python create_admins.py

SETUP: Before running, set these environment variables or edit the ADMINS list below
with the actual credentials (do NOT commit passwords to Git).
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import bcrypt
from dotenv import load_dotenv
load_dotenv()

from app.core.database import SessionLocal
from app.models.models import User, Admin

# Load from environment variables — set these before running
# Example (Windows):  set ADMIN_PASS_1=yourpassword
# Example (Mac/Linux): export ADMIN_PASS_1=yourpassword
ADMINS = [
    {"email": "24071a6737@vnrvjiet.in", "password": os.getenv("ADMIN_PASS_1", ""), "username": "supreeth37",   "name": "Supreeth"},
    {"email": "24071a6741@vnrvjiet.in", "password": os.getenv("ADMIN_PASS_2", ""), "username": "abhilash41",   "name": "Abhilash"},
    {"email": "24071a6743@vnrvjiet.in", "password": os.getenv("ADMIN_PASS_3", ""), "username": "vinayasree43", "name": "Vinayasree"},
    {"email": "24071a6748@vnrvjiet.in", "password": os.getenv("ADMIN_PASS_4", ""), "username": "prasanna48",   "name": "Prasanna"},
]

db = SessionLocal()

for admin_data in ADMINS:
    if not admin_data["password"]:
        print(f"Skipping {admin_data['email']} — no password set. Use ADMIN_PASS_1..4 env vars.")
        continue

    existing = db.query(User).filter(User.email == admin_data["email"]).first()
    if existing:
        print(f"Admin already exists: {admin_data['email']}")
        continue

    hashed = bcrypt.hashpw(admin_data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = User(
        username=admin_data["username"],
        email=admin_data["email"],
        password_hash=hashed,
        role="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    admin = Admin(
        user_id=user.id,
        name=admin_data["name"],
        email=admin_data["email"]
    )
    db.add(admin)
    db.commit()
    print(f"Created admin: {admin_data['email']}")

db.close()
print("Done!")
