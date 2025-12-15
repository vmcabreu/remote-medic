from app import create_app
from app.extensions import db
from flask import Flask
from flask_cors import CORS

app = create_app()
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
