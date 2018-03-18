from flask import Blueprint, abort, jsonify, request, url_for
from sqlalchemy import inspect
from todo import db
from todo.auth import auth
from todo.models import Task


bp = Blueprint('routes', __name__)


def object_as_dict(obj):
    """
    Convert sqlalchemy row object to python dict.

    Reference: https://stackoverflow.com/a/37350445/8074325
    """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def make_public_task(task):
    new_task = {}
    task_dict = object_as_dict(task)
    for field in task_dict:
        if field == 'id':
            new_task['uri'] = url_for(
                'routes.get_task', task_id=task_dict['id'], _external=True)
        else:
            new_task[field] = task_dict[field]
    return new_task


@bp.route('/todo/api/v0.1/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    db_tasks = Task.query.all()
    return jsonify({'tasks': [make_public_task(task) for task in db_tasks]})


@bp.route('/todo/api/v0.1/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    return jsonify({'task': make_public_task(task)})


@bp.route('/todo/api/v0.1/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'title': request.json['title'],
        'description': request.json.get('description', '')
    }
    new_task = Task(**task)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': make_public_task(new_task)}), 201


@bp.route('/todo/api/v0.1/tasks/<int:task_id>', methods=['PATCH'])
@auth.login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()

    return jsonify({'task': make_public_task(task)})


@bp.route('/todo/api/v0.1/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True}), 200
