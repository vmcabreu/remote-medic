import os
from dotenv import load_dotenv

load_dotenv()  # Solo necesario si corres fuera de Docker

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
