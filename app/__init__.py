from flask import Flask
import os
import psycopg2

def create_app():
    app = Flask(__name__)

    app.config['DB_HOST'] = os.environ.get('DB_HOST', 'localhost')
    app.config['DB_NAME'] = os.environ.get('DB_NAME', 'persons')
    app.config['DB_USER'] = os.environ.get('DB_USER', 'user')
    app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD', 'password')

    from .main import main_bp
    app.register_blueprint(main_bp)

    return app
