import pytest

from todo import todo_list

task = 'Task 1'


@pytest.mark.order1
def test_add_task():
    todo_list.add_task(task)
    assert len(todo_list.tasks) == 1


@pytest.mark.order2
def test_complete_task():
    todo_list.mark_task_completed(task)
    assert todo_list.tasks[0].completed


@pytest.mark.order3
def test_delete_task():
    todo_list.delete_task(task)
    assert len(todo_list.tasks) == 0
