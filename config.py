import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-so-secret-key'
    USERNAME = 'admin'
    PASSWORD = 'python'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(app_dir, 'todo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
