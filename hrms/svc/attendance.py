from hrms.prst import model
from sqlmodel import Session, select
import fastapi as fa
import typing as ty


def _session() -> ty.Generator[Session, None, None]:
    with Session(model.engine) as session:
        yield session
        session.commit()


class AttendanceLog:
    def __init__(
        self,
        session: ty.Annotated[
            Session,
            fa.Depends(_session),
        ],
    ):
        self.session = session

    def list(self):
        statement = select(model.AttendanceLog)
        results = self.session.exec(statement)
        attendance_list = results.all()
        return attendance_list

    def get(self, id: int):
        attendance = self.session.get(model.AttendanceLog, id)
        return attendance

    def add(self, attendance_data: model.AttendanceLog):
        attendance = model.AttendanceLog(
            employee_id=attendance_data.employee_id,
            direction=attendance_data.direction,
            time=attendance_data.time,
        )
        self.session.add(attendance)
        return attendance

    def edit(self, id: int, attendance_data: model.AttendanceLog):
        attendance = self.session.get(model.AttendanceLog, id)
        if attendance is not None:
            if attendance_data.employee_id is not None:
                attendance.employee_id = attendance_data.employee_id
            if attendance_data.direction is not None:
                attendance.direction = attendance_data.direction
            if attendance_data.time is not None:
                attendance.time = attendance_data.time
            self.session.add(attendance)
            self.session.commit()
            self.session.refresh(attendance)
            return attendance
        else:
            return {"message": "record not found"}

    def remove(self, id: int):
        attendance = self.session.get(model.AttendanceLog, id)
        if attendance is not None:
            self.session.delete(attendance)
            return attendance
        else:
            return {"message": "record not found"}
