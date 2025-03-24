from flask import Blueprint, request, jsonify, abort
from models import db, User, Event, RSVP

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