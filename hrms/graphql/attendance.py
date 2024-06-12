import strawberry
from hrms.prst import model
from sqlmodel import Session
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from datetime import datetime
from hrms.svc.attendance import AttendanceLog


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
        with Session(model.engine) as session:
            created_attendance = AttendanceLog(session=session).list()
            return [AttendanceType.from_model(att) for att in created_attendance]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_attendance(self, attendance_data: AttendanceTypeInput) -> AttendanceType:
        with Session(model.engine) as session:
            created_attendance = AttendanceLog(session=session).add(
                attendance_data
            )
            return AttendanceType.from_model(created_attendance)

    @strawberry.mutation
    def edit_attendance(
        self, id: int, attendance_data: AttendanceTypeInput
    ) -> Optional[AttendanceType]:
        with Session(model.engine) as session:
            attendance = AttendanceLog(session=session).edit(
                id, attendance_data
            )
            return AttendanceType.from_model(attendance)

    @strawberry.mutation
    def delete_attendance(self, id: int) -> Optional[AttendanceType]:
        with Session(model.engine) as session:
            attendance = AttendanceLog(session=session).remove(id)
            return AttendanceType.from_model(attendance)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_schema3 = GraphQLRouter(schema)
