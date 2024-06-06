import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello() -> str:
        return "world"

@strawberry.type
class Query:
    @strawberry.field
    def hi() -> str:
        return "world hi"

@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        return Book(title=title, author=author)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def restart() -> None:
        print("restarting the server")


schema = strawberry.Schema(query=Query, mutation=Mutation)
