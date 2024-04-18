from fastapi import FastAPI, APIRouter
from repos.repos import UserRepository, IssueRepository, BookRepository
from repos.methods import user_have_book

app = FastAPI(
    title="Library Management App"
)

router = APIRouter()

user_repo = UserRepository()
book_repo = BookRepository()
issue_repo = IssueRepository()


@router.get("/users/read/{user_id}")
async def get_user(user_id: int):
    user = await UserRepository().read_object(id=int(user_id))
    return {
        "First name: ": user[0].first_name,
        "Last name: ": user[0].last_name,
        "Email: ": user[0].email,
        "Books: ": user[0].issues
    }


@router.get("/books/read/{book_id}")
async def get_books(
        book_id: int
):
    book = await book_repo.read_object(id=book_id)
    return {
        "Book id: ": book[0].id,
        "Title: ": book[0].title,
        "Author: ": book[0].author,
        "Publication year: ": book[0].publication_year,
        "Issue: ": book[0].issues
    }


@router.get("/issues/read/{issue_id}")
async def get_issue(
        issue_id: int
):
    issue = await issue_repo.read_object(id=issue_id)
    return {
        "Issue id: ": issue[0].id,
        "Issue date: ": issue[0].issue_date,
        "Return period: ": issue[0].return_period,
        "User: ": issue[0].user,
        "Book: ": issue[0].book
    }


@router.post("/users/update/{user_id}")
async def update_user(user_id: int, fn: str, ln: str, email: str | None = None):
    user = await user_repo.read_object(id=user_id)
    print({"User id: ": {
            "First name: ": user[0].first_name,
            "Last name: ": user[0].last_name,
            "Email: ": user[0].email,
    }})
    await user_repo.update_object(
        user_first_name=user[0].first_name,
        user_last_name=user[0].last_name,
        user_email=user[0].email,
        first_name=fn,
        last_name=ln
    )
    updated_user = await user_repo.read_object(id=user_id)
    return {"User id: ": {
            "First name: ": updated_user[0].first_name,
            "Last name: ": updated_user[0].last_name,
            "Email: ": updated_user[0].email,
    }}

app.include_router(router)
