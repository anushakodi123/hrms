import strawberry
from hrms.api import attendance
from hrms.prst import model
from sqlmodel import Session, select
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import desc
from hrms.svc.attendance import AttendanceLog

# @contextmanager
# def get_session():
#      with Session(model.engine) as session:
#         yield session
#         session.commit()


@strawberry.input
class AttendanceTypeInput:
    employee_id: int
    direction: bool
    time: datetime


@strawberry.type
class AttendanceType:
    id: Optional[int]
    employee_id: int
    direction: bool
    time: datetime

    @staticmethod
    def from_model(attendance: model.AttendanceLog) -> "AttendanceType":
        return AttendanceType(
            id=attendance.id,
            employee_id=attendance.employee_id,
            direction=attendance.direction,
            time=attendance.time,
        )


@strawberry.type
class Query:
    @strawberry.field
    def list_attendance(self) -> List[AttendanceType]:
        created_attendance = AttendanceLog(session=Session(model.engine)).list()
        return [AttendanceType.from_model(att) for att in created_attendance]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_attendance(self, attendance_data: AttendanceTypeInput) -> AttendanceType:
        created_attendance = AttendanceLog(session=Session(model.engine)).add(
            attendance_data
        )
        return AttendanceType.from_model(created_attendance)

    @strawberry.mutation
    def edit_attendance(
        self, id: int, attendance_data: AttendanceTypeInput
    ) -> Optional[AttendanceType]:
        attendance = AttendanceLog(session=Session(model.engine)).edit(
            id, attendance_data
        )
        return AttendanceType.from_model(attendance)

    @strawberry.mutation
    def delete_attendance(self, id: int) -> Optional[AttendanceType]:
        attendance = AttendanceLog(session=Session(model.engine)).remove(id)
        return AttendanceType.from_model(attendance)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_schema3 = GraphQLRouter(schema)
