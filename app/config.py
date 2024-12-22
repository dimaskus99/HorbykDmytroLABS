import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://dimas:dimas88@db/lab3_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "13brh1b3rbuy31gbruy3b")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "23rbi4u2fbiu34hbfui34b")