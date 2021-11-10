from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# DB imports
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
# Logging
import logging

from .config import Config
# ---------- Initial flask config ---------#
app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()
# -----------------------------------------#


# ---------- Initial sqlalchemy config ---------#
def get_engine(url):
    if not database_exists(url):
        create_database(url)

    engine_obj = create_engine(url)
    return engine_obj


# --------------- localhost ---------------
engine = get_engine('postgresql://postgres:566510030912@localhost:5432/GameProject')

# -----------------Docker -----------------
# Switch to the SQLDB_URI in config.py and alembic.ini for further work with Docker
# engine = create_engine(Config.ENGINE_URI)

session = scoped_session(sessionmaker(
    autoflush=False, autocommit=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
# ----------------------------------------------#

# ---------- JWT and cors config ---------#
jwt = JWTManager()

cors = CORS(resources={
    r"/*": {"origins": Config.CORS_ALLOWED_ORIGINS}
})
# -----------------------------------------#


# -------------- Logging ------------------#
def setup_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(message)s'
    )
    file_handler = logging.FileHandler('logs/api.log')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log


logger = setup_logger()
# -----------------------------------------#


# -------------- Main page ------------------#
@app.route('/')
def index():
    return 'Index Page'
# -----------------------------------------#


# -------------- Main error handler ------------------#
@app.errorhandler(422)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
# -----------------------------------------#


# -------------- session handling --------------------#
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
# --------------------------------------------------#


# -------------- Blueprints registration ------------------#
from .companies.companies import api
from .users.users import users

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(api, url_prefix='/api')
# ---------------------------------------------------------#
jwt.init_app(app)
