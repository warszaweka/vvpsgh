from random import randrange

from locust import HttpUser, task, between

tasks = 100


class TodoListUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def view_tasks(self):
        self.client.get('/')

    @task
    def add_task(self):
        self.client.post('/add', data={'task': randrange(tasks)})

    @task
    def delete_task(self):
        self.client.post('/delete', data={'task': randrange(tasks)})

    @task
    def complete_task(self):
        self.client.post('/complete', data={'task': randrange(tasks)})
