from re import S
import strawberry
from hrms.prst import model
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional, Annotated
from sqlalchemy import desc
from contextlib import contextmanager
from hrms.svc.employee import Employee, _session
import fastapi as fa


# def get_session():
#     session = Session(model.engine)
#     try:
#         yield session
#     finally:
#         session.commit()

# def get_employee(session: Annotated[Session, fa.Depends(_session)]):
#     return Employee(session=session)

session = Session(model.engine)

@strawberry.input
class EmployeeTypeInput:
    name: str
    designation: str
    reports_to: Optional[int]
    project: str


@strawberry.type
class EmployeeType:
    id: Optional[int]
    name: str
    designation: str
    reports_to: Optional[int]
    project: str

    @staticmethod
    def from_model(employee: model.Employee) -> "EmployeeType":
        return EmployeeType(
            id=employee.id,
            name=employee.name,
            designation=employee.designation,
            reports_to=employee.reports_to,
            project=employee.project,
        )


@strawberry.type
class Query:
    @strawberry.field
    def list_employees(self) -> List[EmployeeType]:
        employees = Employee(session=session).list()
        return [EmployeeType.from_model(emp) for emp in employees]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_employee(self, employee_data: EmployeeTypeInput) -> EmployeeType:
        employee = Employee(session=session).add(employee_data)
        session.commit()
        return EmployeeType.from_model(employee)

    @strawberry.mutation
    def edit_employee(
        self, id: int, employee_data: EmployeeTypeInput
    ) -> Optional[EmployeeType]:
        employee = Employee(session=Session(model.engine)).edit(id, employee_data)
        session.commit()
        return EmployeeType.from_model(employee)

    @strawberry.mutation
    def delete_employee(self, id: int) -> Optional[EmployeeType]:
        employee = Employee(session=Session(model.engine)).remove(id)
        session.commit()
        return EmployeeType.from_model(employee)


schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_schema2 = GraphQLRouter(schema)
