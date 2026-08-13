"""
Run once after the DB is up to create initial user accounts.
Usage: python seed.py
"""
from app.database import SessionLocal, engine, Base
from app import models, auth

Base.metadata.create_all(bind=engine)
db = SessionLocal()

users = [
    {"name": "Admin User", "email": "admin@example.com", "password": "changeme123", "role": "admin"},
    {"name": "Rep One", "email": "rep1@example.com", "password": "changeme123", "role": "rep"},
    {"name": "Rep Two", "email": "rep2@example.com", "password": "changeme123", "role": "rep"},
]

for u in users:
    existing = db.query(models.User).filter(models.User.email == u["email"]).first()
    if existing:
        print(f"Skipping {u['email']} - already exists")
        continue
    db_user = models.User(
        name=u["name"],
        email=u["email"],
        hashed_password=auth.hash_password(u["password"]),
        role=u["role"],
    )
    db.add(db_user)
    print(f"Created {u['email']}")

db.commit()
db.close()
print("Seed complete. CHANGE THESE PASSWORDS after first login.")
