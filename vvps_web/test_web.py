import subprocess
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    process = subprocess.Popen(['/usr/bin/zsh', '-c', 'pipenv run python todo.py'], cwd='../vvps')
    driver = webdriver.Chrome()
    time.sleep(3)
    yield driver
    driver.quit()
    process.terminate()


def test_add_task(browser):
    task = 'Task 1'
    browser.get('http://localhost:5000')
    time.sleep(1)
    add_input = browser.find_element(By.ID, 'add-input')
    add_input.send_keys(task)
    add_input.send_keys(Keys.RETURN)
    time.sleep(1)
    task_list = browser.find_element(By.TAG_NAME, 'ul')
    tasks = task_list.find_elements(By.TAG_NAME, 'li')
    assert len(tasks) == 1
    assert tasks[0].find_element(By.TAG_NAME, 'span').text == task


def test_delete_task(browser):
    task = 'Task 2'
    browser.get('http://localhost:5000')
    time.sleep(1)
    add_input = browser.find_element(By.ID, 'add-input')
    add_input.send_keys(task)
    add_input.send_keys(Keys.RETURN)
    time.sleep(1)
    delete_button = browser.find_element(By.CLASS_NAME, 'delete-button')
    delete_button.click()
    time.sleep(1)
    task_list = browser.find_element(By.TAG_NAME, 'ul')
    tasks = task_list.find_elements(By.TAG_NAME, 'li')
    assert len(tasks) == 0


def test_complete_task(browser):
    task = 'Task 3'
    browser.get('http://localhost:5000')
    time.sleep(1)
    add_input = browser.find_element(By.ID, 'add-input')
    add_input.send_keys(task)
    add_input.send_keys(Keys.RETURN)
    time.sleep(1)
    complete_button = browser.find_element(By.CLASS_NAME, 'complete-button')
    complete_button.click()
    time.sleep(1)
    completed_task = browser.find_element(By.CLASS_NAME, 'completed')
    assert completed_task.is_displayed()
