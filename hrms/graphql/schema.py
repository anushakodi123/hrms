import strawberry
from strawberry.fastapi import GraphQLRouter

from hrms.graphql import attendance, employee, holiday, leave

@strawberry.type
class Query(attendance.Query, employee.Query, holiday.Query, leave.Query):
    pass

@strawberry.type
class Mutation(attendance.Mutation, employee.Mutation, holiday.Mutation, leave.Mutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
router = GraphQLRouter(schema)


