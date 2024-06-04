from sqlmodel import SQLModel, Field, create_engine
from datetime import datetime
import enum

class LeaveType(enum.StrEnum):
    SICK = "sick"
    CASUAL = "casual"

class Employee(SQLModel, table=True):   
    id: int | None = Field(default=None, primary_key=True)
    name: str
    designation: str
    reports_to: int | None = Field(default=None, foreign_key="employee.id")
    project: str

class AttendanceLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employee_id: int = Field(default=None, foreign_key="employee.id")
    direction: bool | None
    time: datetime | None = None

class Leave(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    employee_id: int = Field(default=None, foreign_key="employee.id")
    type: LeaveType
    time: datetime

class Holiday(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    on: datetime

engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)