import strawberry


def get_name() -> str:
    return "strawberry"


# @strawberry.type
# class Query:
#     name: str = strawberry.field(resolver=get_name)


@strawberry.type
class Query:
    @strawberry.field
    def name(self) -> str:
        return "strawberry"


schema = strawberry.Schema(query=Query)
