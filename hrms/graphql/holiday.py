import datetime
import strawberry
from hrms.prst import model
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from sqlalchemy import desc
from contextlib import contextmanager
from datetime import datetime
from hrms.svc.holiday import Holiday

# @contextmanager
# def get_session():
#     session = Session(model.engine)
#     try:
#         yield session
#     finally:
#         session.commit()


@strawberry.input
class HolidayTypeInput:
    name: str
    on: datetime


@strawberry.type
class HolidayType:
    id: Optional[int]
    name: str
    on: datetime

    @staticmethod
    def from_model(holiday: model.Holiday) -> "HolidayType":
        return HolidayType(id=holiday.id, name=holiday.name, on=holiday.on)


@strawberry.type
class Query:
    @strawberry.field
    def list_holidays(self) -> List[HolidayType]:
        holidays = Holiday(session=Session(model.engine)).list()
        return [HolidayType.from_model(holi) for holi in holidays]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_holidays(self, holiday_data: HolidayTypeInput) -> HolidayType:
        created_holiday = Holiday(session=Session(model.engine)).add(holiday_data)
        return HolidayType.from_model(created_holiday)

    @strawberry.mutation
    def edit_holiday(
        self, id: int, holiday_data: HolidayTypeInput
    ) -> Optional[HolidayType]:
        holiday = Holiday(session=Session(model.engine)).edit(id, holiday_data)
        return HolidayType.from_model(holiday)

    @strawberry.mutation
    def delete_holiday(self, id: int) -> Optional[HolidayType]:
        holiday = Holiday(session=Session(model.engine)).remove(id)
        return HolidayType.from_model(holiday)


schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_schema5 = GraphQLRouter(schema)
