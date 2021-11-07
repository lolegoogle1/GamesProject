import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
    JWT_SECRET_KEY='aedc1463ac5e4fbaba4b097d73b3a0e5'
