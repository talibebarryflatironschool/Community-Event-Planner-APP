# #!/usr/bin/env python3

# # Standard library imports
# from random import randint, choice as rc

# # Remote library imports
# from faker import Faker

# # Local imports
# from app import app
# from models import db

# if __name__ == '__main__':
#     fake = Faker()
#     with app.app_context():
#         print("Starting seed...")
#         # Seed code goes here!




#!/usr/bin/env python3
# seed.py

from app import app, db
from models import User, Event
from datetime import datetime

def seed_data():
    with app.app_context():
        # Create test user
        user = User(username='test', email='test@example.com')
        db.session.add(user)
        
        # Create sample event
        event = Event(
            title='Community Cleanup',
            date=datetime(2024, 3, 15),
            location='Central Park',
            creator_id=1
        )
        db.session.add(event)
        
        db.session.commit()