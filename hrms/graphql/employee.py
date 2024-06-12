import strawberry
from hrms.prst import model
from sqlmodel import Session
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from hrms.svc.employee import Employee

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
        with Session(model.engine) as session:
            employees = Employee(session=session).list()
            return [EmployeeType.from_model(emp) for emp in employees]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_employee(self, employee_data: EmployeeTypeInput) -> EmployeeType:
        with Session(model.engine) as session:
            employee = Employee(session=session).add(employee_data)
            return EmployeeType.from_model(employee)

    @strawberry.mutation
    def edit_employee(
        self, id: int, employee_data: EmployeeTypeInput
    ) -> Optional[EmployeeType]:
        with Session(model.engine) as session:
            employee = Employee(session=session).edit(id, employee_data)
            return EmployeeType.from_model(employee)

    @strawberry.mutation
    def delete_employee(self, id: int) -> Optional[EmployeeType]:
        with Session(model.engine) as session:
            employee = Employee(session=session).remove(id)
            return EmployeeType.from_model(employee)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_schema2 = GraphQLRouter(schema)
