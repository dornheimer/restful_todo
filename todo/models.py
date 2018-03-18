from todo import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text())
    done = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        class_name = type(self).__name__
        return f"<{class_name} '{self.title}'>"
