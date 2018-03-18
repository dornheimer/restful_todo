import unittest
import base64
import json
from todo import create_app, db
from config import Config
from populate_db import populate_db


class TestConfig(Config):
    USERNAME = 'test_user'
    PASSWORD = 'test_pw'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestRoutes(unittest.TestCase):

    def make_auth_header(self):
        user = self.app.config['USERNAME']
        pw = self.app.config['PASSWORD']
        creds = bytes("{}:{}".format(user, pw), 'utf-8')
        creds64 = base64.b64encode(creds).decode('utf-8')
        return {'Authorization': f'Basic {creds64}'}

    def get_response(self, url, method, auth=True, **kwargs):
        methods = {'GET': self.client.get,
                   'POST': self.client.post,
                   'PATCH': self.client.patch,
                   'DELETE': self.client.delete}

        if auth:
            if 'headers' in kwargs:
                kwargs['headers'].update(self.make_auth_header())
            else:
                kwargs['headers'] = self.make_auth_header()

        return methods[method](url, **kwargs)

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_tasks_empty_db(self):
        response = self.get_response('/todo/api/v0.1/tasks', 'GET')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'tasks': []})

    def test_get_tasks_populated_db(self):
        populate_db()
        response = self.get_response('/todo/api/v0.1/tasks', 'GET')
        response_data = json.loads(response.data)
        num_tasks = len(response_data['tasks'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(num_tasks, 5)
        self.assertFalse(response_data['tasks'][0]['done'])
        self.assertTrue(response_data['tasks'][-1]['uri'].endswith('5'))

    def test_get_task_id(self):
        populate_db()
        response = self.get_response('/todo/api/v0.1/tasks/5', 'GET')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("task" in response_data)
        self.assertTrue(response_data['task']['uri'].endswith('5'))

    def test_get_task_id_not_found(self):
        populate_db()
        response = self.get_response('/todo/api/v0.1/tasks/6', 'GET')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data, {"error": "Not found"})

    def test_create_task(self):
        task = json.dumps({"title": "test task", "description": "a test task"})
        headers = {'Content-Type': 'application/json'}
        response = self.get_response(
            '/todo/api/v0.1/tasks', 'POST', data=task, headers=headers)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("task" in response_data)
        self.assertTrue(response_data['task']['uri'].endswith('1'))
        self.assertFalse(response_data['task']['done'])

    def test_create_task_missing_title(self):
        task = json.dumps({"description": "a test task"})
        headers = {'Content-Type': 'application/json'}
        response = self.get_response(
            '/todo/api/v0.1/tasks', 'POST', data=task, headers=headers)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'error': 'Bad request'})

    def test_create_task_not_json(self):
        task = {"title": "test task", "description": "a test task"}
        response = self.get_response(
            '/todo/api/v0.1/tasks', 'POST', data=task)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'error': 'Bad request'})

    def test_create_task_successive(self):
        task = {"title": "test task", "description": "a test task"}
        task2 = {"title": "test task2", "description": "another test task"}
        headers = {'Content-Type': 'application/json'}

        for t_id, t in enumerate((task, task2), 1):
            response = self.get_response(
                '/todo/api/v0.1/tasks', 'POST',
                data=json.dumps(task),
                headers=headers)
            response_data = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertTrue("task" in response_data)
            self.assertFalse(response_data['task']['done'])
            self.assertTrue(response_data['task']['uri'].endswith(str(t_id)))

    def test_update_task(self):
        populate_db()
        update = {"done": True}
        headers = {'Content-Type': 'application/json'}
        response = self.get_response(
            '/todo/api/v0.1/tasks/5', 'PATCH',
            data=json.dumps(update), headers=headers)
        response_data = json.loads(response.data)
        #self.assertEqual(response.status_code, 204)
        self.assertTrue(response_data['task']['done'])

    def test_delete_task(self):
        populate_db()
        response = self.get_response('/todo/api/v0.1/tasks/5', 'DELETE')
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {"result": True})


if __name__ == '__main__':
    unittest.main()
