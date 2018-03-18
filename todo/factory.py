from flask import Flask
from werkzeug.utils import find_modules, import_string
from todo import db, migrate
from config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules.

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('todo.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None
