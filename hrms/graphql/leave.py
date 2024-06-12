from email.headerregistry import DateHeader
import strawberry
from hrms.prst import model
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from sqlalchemy import desc
from contextlib import contextmanager
from datetime import datetime
from hrms.svc.leave import Leave

# @contextmanager
# def get_session():
#     session = Session(model.engine)
#     try:
#         yield session
#     finally:
#         session.commit()


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
        leaves = Leave(session=Session(model.engine)).list()
        return [LeaveType.from_model(leave) for leave in leaves]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_leaves(self, leave_data: LeaveTypeInput) -> LeaveType:
        leave = Leave(session=Session(model.engine)).add(leave_data)
        # session.commit()
        # statement = select(model.Employee).order_by(desc(model.Employee.id)).limit(1)
        # result = session.exec(statement)
        # created_employee = result.first()
        return LeaveType.from_model(leave)

    @strawberry.mutation
    def edit_leave(self, id: int, leave_data: LeaveTypeInput) -> Optional[LeaveType]:
        leave = Leave(session=Session(model.engine)).edit(id, leave_data)
        return LeaveType.from_model(leave)

    @strawberry.mutation
    def delete_leave(self, id: int) -> Optional[LeaveType]:
        leave = Leave(session=Session(model.engine)).remove(id)
        return LeaveType.from_model(leave)


schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_schema4 = GraphQLRouter(schema)
