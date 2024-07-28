import json
import os
from github import Github


def get_pull_request_info():
    # Получение значения GITHUB_TOKEN из переменной окружения
    access_token = os.getenv('GITHUB_TOKEN')

    # Инициализация объекта Github с использованием токена доступа
    g = Github(access_token)

    # Получение контекста события
    event_path = os.getenv('GITHUB_EVENT_PATH')
    with open(event_path, 'r') as event_file:
        event_data = json.load(event_file)

    # Получение данных о репозитории и PR из контекста события
    repo_name = event_data['repository']['full_name']
    pr_number = event_data['number']

    # Получение репозитория и PR
    repo = g.get_repo(repo_name)
    pull_request = repo.get_pull(pr_number)

    # Вывод информации о PR
    print(f"Title: {pull_request.title}")
    print(f"Body: {pull_request.body}")
    print(f"Author: {pull_request.user.login}")
    print(f"URL: {pull_request.html_url}")

    # Получение файлов из PR
    pr_files = pull_request.get_files()
    for file in pr_files:
        print(f"File: {file.filename}")
        print(f"Status: {file.status}")
        print(f"Additions: {file.additions}")
        print(f"Deletions: {file.deletions}")
        print(f"Changes: {file.changes}")