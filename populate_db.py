from todo import db
from todo.models import Task


def populate_db():
    tasks = [Task(title="test", description="test task") for i in range(5)]
    for t in tasks:
        db.session.add(t)
    db.session.commit()
