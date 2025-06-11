# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
import json
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake(id):
    print(id)
    eq = Earthquake.query.filter_by(id=id).first()
    if eq:
        data = {
        "id": eq.id,
        "magnitude": eq.magnitude,
        "location": eq.location,
        "year": eq.year
        }
        res = 200
    else:
        data = {
            "message": f"Earthquake {id} not found."
        }
        res = 404
    return make_response(jsonify(data), res)

@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_magnitude(magnitude):
    eq = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if len(eq):
        data = {
            "count": len(eq),
            "quakes": []
        }
        for e in eq:
            data['quakes'].append({
                "id": e.id,
                "location": e.location,
                "magnitude": e.magnitude,
                "year": e.year
            })

        res = 200
    else:
        data = {
            "count": len(eq),
            "quakes": []
        }
        res = 200
    return make_response(jsonify(data), res)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
