import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "my-secret-key"
    # "The secret key is used to securely sign sessions,
    #  cookies, and Flask flash messages. It helps prevent 
    # users from tampering with session data."

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "trekking.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False