import eventlet

eventlet.monkey_patch()

import eventlet.wsgi
from flask import Flask, render_template, request
from flask_socketio import SocketIO


class TodoItem:

    def __init__(self, task):
        self.task = task
        self.completed = False


class TodoList:

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(TodoItem(task))

    def delete_task(self, task):
        for item in self.tasks:
            if item.task == task:
                self.tasks.remove(item)
                break

    def mark_task_completed(self, task):
        for item in self.tasks:
            if item.task == task:
                item.completed = True
                break


todo_list = TodoList()
app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html', tasks=todo_list.tasks)


@app.route('/add', methods=['POST'])
def add_task():
    todo_list.add_task(request.form.get('task'))
    socketio.emit('update')
    return '', 204


@app.route('/delete', methods=['POST'])
def delete_task():
    todo_list.delete_task(request.form.get('task'))
    socketio.emit('update')
    return '', 204


@app.route('/complete', methods=['POST'])
def complete_task():
    todo_list.mark_task_completed(request.form.get('task'))
    socketio.emit('update')
    return '', 204


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
