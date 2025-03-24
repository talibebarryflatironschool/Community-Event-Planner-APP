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
from models import db
from flask_migrate import Migrate
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run(port=5555, debug=True)