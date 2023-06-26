import csv

import pytest

from todo import TodoList


def read_test_data(file_path):
    test_data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            commands = [tuple(command.split(',')) for command in row[0].split(';')]
            expected_tasks = []
            if row[1]:
                expected_tasks = [(lambda task, completed: (task, completed == 'True'))(*expected_task.split(',')) for expected_task in row[1].split(';')]
            test_data.append((commands, expected_tasks))
    return test_data


@pytest.fixture
def todo_list():
    return TodoList()


@pytest.mark.parametrize(('commands', 'expected_tasks'), read_test_data('data.csv'))
def test_todo_list_operations(todo_list, commands, expected_tasks):
    for command in commands:
        operation, task = command
        if operation == 'add':
            todo_list.add_task(task)
        elif operation == 'delete':
            todo_list.delete_task(task)
        elif operation == 'complete':
            todo_list.mark_task_completed(task)

    tasks = [(item.task, item.completed) for item in todo_list.tasks]
    assert tasks == expected_tasks
