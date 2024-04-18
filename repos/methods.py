import datetime

from .models import User, Book, Issue
from .repos import UserRepository, IssueRepository, BookRepository, BaseRepository

user_repo = UserRepository()
book_repo = BookRepository()
issue_repo = IssueRepository()


async def add_user(*, first_name: str, last_name: str, email: str):
    await user_repo.insert_object(
        User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
    )


async def add_book(*, title: str, author: str, publication_year: int):
    await book_repo.insert_object(
        Book(
            title=title,
            author=author,
            publication_year=publication_year
        )
    )


async def add_issue(*, user_id: int, book_id: int):
    await issue_repo.insert_object(
        Issue(
            user_id=user_id,
            book_id=book_id
        )
    )


async def user_have_book(*, user_id: int):
    user = await user_repo.read_object(
        id=user_id
    )
    if len(user) > 1:
        print("Object more than one")
    elif len(user) == 0:
        print("User not found")
    else:
        return await book_repo.read_object(id=user[0].issues.book_id)



async def users_overdue_return():
    users = []
    issue = await issue_repo.read_object()
    for item in issue:
        if item.return_period < datetime.date.today():
            users.append(item.user_id)

    return [await user_repo.read_object(id=user_id) for user_id in users]


async def most_popular_book():
    books = {}
    issue = await issue_repo.read_object()
    for item in issue:
        new_issue = await issue_repo.read_object(book_id=item.book_id)
        books[len(new_issue)] = item.book_id

    most_popular = await book_repo.read_object(id=books[max(books)])
    return most_popular


async def task_run():
    books = await user_have_book(user_fn="Ihor", user_ln="Shkrob", user_email="lalala@gmail.com")
    for item in books:
        print(item.id, item.title, item.author, item.publication_year)
    users = await users_overdue_return()
    for item in users:
        print(item[0].first_name, item[0].last_name)
    book = await most_popular_book()
    for item in book:
        print(item.title)


