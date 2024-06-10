import strawberry
from hrms.prst import model
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from sqlalchemy import desc
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session(model.engine)
    try:
        yield session
    finally:
        session.commit()

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
        with get_session() as session:
            statement = select(model.Employee)
            results = session.exec(statement)
            employees = results.all()
            return [EmployeeType.from_model(emp) for emp in employees]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_employee(self, employee_data: EmployeeTypeInput) -> EmployeeType:
        with get_session() as session:
            employee = model.Employee(
                name=employee_data.name,
                designation=employee_data.designation,
                reports_to=employee_data.reports_to,
                project=employee_data.project,
            )
            session.add(employee)

            # Fetch the newly created employee
            statement = select(model.Employee).order_by(desc(model.Employee.id)).limit(1)
            result = session.exec(statement)
            created_employee = result.first()
            return EmployeeType.from_model(created_employee)

    @strawberry.mutation
    def edit_employee(self, id: int, employee_data: EmployeeTypeInput) -> Optional[EmployeeType]:
        with get_session() as session:
            employee = session.get(model.Employee, id)
            if employee is not None:
                if employee_data.name is not None:
                    employee.name = employee_data.name
                if employee_data.designation is not None:
                    employee.designation = employee_data.designation
                if employee_data.reports_to is not None:
                    employee.reports_to = employee_data.reports_to
                if employee_data.project is not None:
                    employee.project = employee_data.project
                session.add(employee)
                session.refresh(employee)
                return EmployeeType.from_model(employee)
            return None

    @strawberry.mutation
    def delete_employee(self, id: int) -> Optional[EmployeeType]:
        with get_session() as session:
            employee = session.get(model.Employee, id)
            if employee is not None:
                session.delete(employee)
                return EmployeeType.from_model(employee)
            return None


schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_schema2 = GraphQLRouter(schema)
