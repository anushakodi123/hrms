import strawberry
from hrms.prst import model
from sqlmodel import Session
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from datetime import datetime
from hrms.svc.leave import Leave

@strawberry.input
class LeaveTypeInput:
    employee_id: int
    type: str
    time: datetime


@strawberry.type
class LeaveType:
    id: Optional[int]
    employee_id: int
    type: str
    time: datetime

    @staticmethod
    def from_model(leave: model.Leave) -> "LeaveType":
        return LeaveType(
            id=leave.id, employee_id=leave.employee_id, type=leave.type, time=leave.time
        )


@strawberry.type
class Query:
    @strawberry.field
    def list_leaves(self) -> List[LeaveType]:
        with Session(model.engine) as session:
            leaves = Leave(session=session).list()
            return [LeaveType.from_model(leave) for leave in leaves]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_leaves(self, leave_data: LeaveTypeInput) -> LeaveType:
        with Session(model.engine) as session:
            leave = Leave(session=session).add(leave_data)
            return LeaveType.from_model(leave)

    @strawberry.mutation
    def edit_leave(self, id: int, leave_data: LeaveTypeInput) -> Optional[LeaveType]:
        with Session(model.engine) as session:
            leave = Leave(session=session).edit(id, leave_data)
            return LeaveType.from_model(leave)

    @strawberry.mutation
    def delete_leave(self, id: int) -> Optional[LeaveType]:
        with Session(model.engine) as session:
            leave = Leave(session=session).remove(id)
            return LeaveType.from_model(leave)


schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_schema4 = GraphQLRouter(schema)
