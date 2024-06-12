from hrms.prst import model
from sqlmodel import Session, select
import fastapi as fa
import typing as ty


def _session():
    with Session(model.engine) as session:
        yield session
        session.commit()


class Employee:
    def __init__(
        self,
        session: ty.Annotated[
            Session,
            fa.Depends(_session),
        ],
    ):
        self.session = session

    def list(self):
        statement = select(model.Employee)
        results = self.session.exec(statement)
        employees = results.all()
        return employees

    def get(self, id: int):
        employee = self.session.get(model.Employee, id)
        return employee

    def add(self, employee_data: model.Employee):
        employee = model.Employee(
            name=employee_data.name,
            designation=employee_data.designation,
            reports_to=employee_data.reports_to,
            project=employee_data.project,
        )
        self.session.add(employee)
        return employee

    def edit(self, id: int, employee_data: model.Employee):
        employee = self.session.get(model.Employee, id)
        if employee is not None:
            if employee_data.name is not None:
                employee.name = employee_data.name
            if employee_data.designation is not None:
                employee.designation = employee_data.designation
            if employee_data.reports_to is not None:
                employee.reports_to = employee_data.reports_to
            if employee_data.project is not None:
                employee.project = employee_data.project
            self.session.add(employee)
            self.session.refresh(employee)
            return employee
        else:
            return {"message": "record not found"}

    def remove(self, id: int):
        employee = self.session.get(model.Employee, id)
        if employee is not None:
            self.session.delete(employee)
            return employee
