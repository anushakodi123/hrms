from hrms.prst import model
from sqlmodel import Session, select
import fastapi as fa
import typing as ty


def _session():
    with Session(model.engine) as session:
        yield session
        session.commit()


class Leave:
    def __init__(
        self,
        session: ty.Annotated[
            Session,
            fa.Depends(_session),
        ],
    ):
        self.session = session

    def list(self):
        statement = select(model.Leave)
        results = self.session.exec(statement)
        leaves = results.all()
        return leaves

    def get(self, id: int):
        leave = self.session.get(model.Leave, id)
        return leave

    def add(self, leave_data: model.Leave):
        leave = model.Leave(
            employee_id=leave_data.employee_id,
            type=leave_data.type,
            time=leave_data.time
        )
        self.session.add(leave)

        return leave

    def edit(self, id: int, leave_data: model.Leave):
        leave = self.session.get(model.Leave, id)
        if leave is not None:
            if leave_data.employee_id is not None:
                leave.employee_id = leave_data.employee_id
            if leave_data.type is not None:
                leave.type = leave_data.type
            if leave_data.time is not None:
                leave.time =leave_data.time
            self.session.add(leave)
            self.session.commit()
            self.session.refresh(leave)
            return leave
        else:
            return {"message": "record not found"}

    def remove(self, id: int):
        leave = self.session.get(model.Leave, id)
        if leave is not None:
            self.session.delete(leave)
            return leave
