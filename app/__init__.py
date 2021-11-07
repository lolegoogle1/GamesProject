from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from flask_jwt_extended import JWTManager

from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
# Logging
import logging


app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()


def get_engine(url):
    if not database_exists(url):
        create_database(url)

    engine_obj = create_engine(url)
    return engine_obj


engine = Config.SQLALCHEMY_DATABASE_URI

session = scoped_session(sessionmaker(
    autoflush=False, autocommit=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

cors = CORS(resources={
    r"/*": {"origins": Config.CORS_ALLOWED_ORIGINS}
})


# -------------- Logging ----------------
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(message)s'
    )
    file_handler = logging.FileHandler('logs/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
# --------------------------------------


@app.route('/')
def index():
    return 'Index Page'


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@app.errorhandler(422)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from .companies.companies import api

app.register_blueprint(api, url_prefix='/api')