import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    ENGINE_URI = 'postgresql://postgres:566510030912@localhost:5432/GameProject'
    CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
    JWT_SECRET_KEY = 'aedc1463ac5e4fbaba4b097d73b3a0e5'
