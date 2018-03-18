from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from todo import models
from todo.factory import create_app
from populate_db import populate_db

app = create_app()


@app.cli.command('populate_db')
def command_populate_db():
    populate_db()
    print("Added entries to database.")
