# # #!/usr/bin/env python3

# # # Standard library imports

# # # Remote library imports
# # from flask import request
# # from flask_restful import Resource

# # # Local imports
# # from config import app, db, api
# # # Add your model imports


# # # Views go here!

# # @app.route('/')
# # def index():
# #     return '<h1>Project Server</h1>'


# # if __name__ == '__main__':
# #     app.run(port=5555, debug=True)







# # app.py

# from config import app, db, api
# from flask import request
# from flask_restful import Resource
# from models import Event
# from datetime import datetime

# class EventListResource(Resource):
#     def get(self):
#         events = Event.query.all()
#         return [event.to_dict() for event in events], 200
    
#     def post(self):
#         data = request.get_json()
#         new_event = Event(
#             title=data.get('title'),
#             description=data.get('description'),
#             date=datetime.fromisoformat(data.get('date')),
#             location=data.get('location'),
#             creator_id=data.get('creator_id')
#         )
#         db.session.add(new_event)
#         db.session.commit()
#         return new_event.to_dict(), 201

# class EventResource(Resource):
#     def get(self, event_id):
#         event = Event.query.get_or_404(event_id)
#         return event.to_dict(), 200
    
#     def put(self, event_id):
#         data = request.get_json()
#         event = Event.query.get_or_404(event_id)
#         event.title = data.get('title', event.title)
#         event.description = data.get('description', event.description)
#         if data.get('date'):
#             event.date = datetime.fromisoformat(data.get('date'))
#         event.location = data.get('location', event.location)
#         db.session.commit()
#         return event.to_dict(), 200

#     def delete(self, event_id):
#         event = Event.query.get_or_404(event_id)
#         db.session.delete(event)
#         db.session.commit()
#         return {'message': 'Event deleted'}, 200

# # Register endpoints
# api.add_resource(EventListResource, '/api/events')
# api.add_resource(EventResource, '/api/events/<int:event_id>')

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)






from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Blueprint, request, jsonify, abort
from models import db, User, Event, RSVP

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    # Register API routes
    from routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

app = create_app()



bp = Blueprint('routes', __name__, url_prefix='/api')

# ----- User Endpoints -----

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        abort(400, description="Missing required fields")
    # Check if user exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        abort(400, description="User already exists")
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        abort(401, description="Invalid credentials")
    # For simplicity, return user data. (In production, implement token-based authentication.)
    return jsonify(user.to_dict()), 200

# ----- Event Endpoints -----

@bp.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'GET':
        events = Event.query.all()
        return jsonify([e.to_dict() for e in events])
    elif request.method == 'POST':
        data = request.get_json()
        # Validate required fields
        for field in ['title', 'description', 'date', 'location', 'creator_id']:
            if field not in data:
                abort(400, description=f"Missing {field}")
        new_event = Event(
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location'],
            creator_id=data['creator_id']
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201

@bp.route('/events/<int:event_id>', methods=['GET', 'PATCH', 'DELETE'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'GET':
        return jsonify(event.to_dict())
    elif request.method == 'PATCH':
        data = request.get_json()
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = data['date']
        if 'location' in data:
            event.location = data['location']
        db.session.commit()
        return jsonify(event.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted"})

# ----- RSVP Endpoints -----

@bp.route('/rsvps', methods=['GET', 'POST'])
def rsvps():
    if request.method == 'GET':
        rsvps = RSVP.query.all()
        return jsonify([r.to_dict() for r in rsvps])
    elif request.method == 'POST':
        data = request.get_json()
        for field in ['user_id', 'event_id', 'response']:
            if field not in data:
                abort(400, description=f"Missing {field}")
        new_rsvp = RSVP(
            user_id=data['user_id'],
            event_id=data['event_id'],
            response=data['response']
        )
        db.session.add(new_rsvp)
        db.session.commit()
        return jsonify(new_rsvp.to_dict()), 201

@bp.route('/rsvps/<int:rsvp_id>', methods=['GET', 'PATCH', 'DELETE'])
def rsvp_detail(rsvp_id):
    rsvp = RSVP.query.get_or_404(rsvp_id)
    if request.method == 'GET':
        return jsonify(rsvp.to_dict())
    elif request.method == 'PATCH':
        data = request.get_json()
        if 'response' in data:
            rsvp.response = data['response']
        db.session.commit()
        return jsonify(rsvp.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(rsvp)
        db.session.commit()
        return jsonify({"message": "RSVP deleted"})


if __name__ == '__main__':
    app.run(port=5555, debug=True)