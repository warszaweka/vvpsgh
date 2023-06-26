import unittest
from unittest.mock import patch

import todo


class TodoListTests(unittest.TestCase):

    def setUp(self):
        self.client = todo.app.test_client()
        todo.todo_list = todo.TodoList()

    def test_add_task(self):
        task = 'Task 1'

        with patch('todo.socketio') as mock_socketio:
            response = self.client.post('/add', data={'task': task})

            self.assertEqual(response.status_code, 204)

            self.assertEqual(len(todo.todo_list.tasks), 1)
            self.assertEqual(todo.todo_list.tasks[0].task, task)

            mock_socketio.emit.assert_called_once_with('update')

    def test_delete_task(self):
        task = 'Task 2'
        todo.todo_list.add_task(task)

        with patch('todo.socketio') as mock_socketio:
            response = self.client.post('/delete', data={'task': task})

            self.assertEqual(response.status_code, 204)

            self.assertEqual(len(todo.todo_list.tasks), 0)

            mock_socketio.emit.assert_called_once_with('update')

    def test_mark_task_completed(self):
        task = 'Task 3'
        todo.todo_list.add_task(task)

        with patch('todo.socketio') as mock_socketio:
            response = self.client.post('/complete', data={'task': task})

            self.assertEqual(response.status_code, 204)

            self.assertTrue(todo.todo_list.tasks[0].completed)

            mock_socketio.emit.assert_called_once_with('update')
