from hrms.api import holiday
from hrms.prst import model
from sqlmodel import Session, select
import fastapi as fa
import typing as ty


def _session():
    with Session(model.engine) as session:
        yield session
        session.commit()


class Holiday:
    def __init__(
        self,
        session: ty.Annotated[
            Session,
            fa.Depends(_session),
        ],
    ):
        self.session = session

    def list(self):
        statement = select(model.Holiday)
        results = self.session.exec(statement)
        holidays = results.all()
        return holidays

    def get(self, id: int):
        holiday = self.session.get(model.Holiday, id)
        return holiday

    def add(self, holiday_data: model.Holiday):
        holiday = model.Holiday(
            name=holiday_data.name,
            on=holiday_data.on
        )
        self.session.add(holiday)
        return holiday

    def edit(self, id: int, holiday_data: model.Holiday):
        holiday = self.session.get(model.Holiday, id)
        if holiday is not None:
            if holiday_data.name is not None:
                holiday.name = holiday_data.name
            if holiday_data.on is not None:
                holiday.on = holiday_data.on
            self.session.add(holiday)
            self.session.commit()
            self.session.refresh(holiday)
            return holiday
        else:
            return {"message": "record not found"}

    def remove(self, id: int):
        holiday = self.session.get(model.Holiday, id)
        if holiday is not None:
            self.session.delete(holiday)
            return holiday
