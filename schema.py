import typing
import strawberry


def get_author_for_book() -> "Author":
    return Author(name="Michael Crichton")

@strawberry.type
class Book:
    title: str
    author: "Author"


def get_books_for_author(root) -> typing.List[Book]:
    return [Book(title="The Great Gatsby", author=root)]

@strawberry.type
class Author:
    name: str
    books: typing.List[Book] = strawberry.field(resolver=get_books_for_author)


def get_authors(root) -> typing.List[Author]:
    return [Author(name="Michael Crichton")]

@strawberry.type
class Query:
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    books: typing.List[Book] = strawberry.field(resolver=lambda root: get_books_for_author(root))

@strawberry.input
class AddBookInput:
    title: str
    author: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, book: AddBookInput) -> Book:
        new_author = Author(name=book.author)
        new_book = Book(title=book.title, author=new_author)
        return new_book


schema = strawberry.Schema(query=Query, mutation=Mutation)
