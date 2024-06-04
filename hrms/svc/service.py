from hrms.prst import model
from sqlmodel import Session, select

class Employee:
    def list(self):
        with Session(model.engine) as session:
            statement = select(model.Employee)
            results = session.exec(statement)
            employees = results.all()
            return employees
        
    def get(self, id: int):
        with Session(model.engine) as session:
            statement = select(model.Employee).where(model.Employee.id == id)
            results = session.exec(statement)
            record = results.first()
            if record is not None:
                return record
            else:
                return {"message": "record not found"}

    def add(self, name: str, designation: str, reports_to: int, project: str):
        employee = model.Employee(name=name, designation=designation, reports_to=reports_to, project=project)
        with Session(model.engine) as session:
            session.add(employee)
            session.commit()
            return {"message": "employee added successfully"}

    def edit(self, id: int, name: str = None, designation: str = None, reports_to: int = None, project: str = None):
        with Session(model.engine) as session:
            statement = select(model.Employee).where(model.Employee.id == id)
            results = session.exec(statement)
            employee = results.one()
            if employee is not None:
                if name is not None:
                    employee.name = name
                if designation is not None:
                    employee.designation = designation
                if reports_to is not None:
                    employee.reports_to = reports_to
                if project is not None:
                    employee.project = project
                session.add(employee)
                session.commit()
                session.refresh(employee)
                return employee
            else:
                return {"message": "record not found"}

    def remove(self, id: int):
        with Session(model.engine) as session:
            statement = select(model.Employee).where(model.Employee.id == id)
            results = session.exec(statement)
            employee = results.one()
            if employee is not None:
                session.delete(employee)
                session.commit()
                return {"message": "record deleted"}
            else:
                return {"message": "record not found"}
