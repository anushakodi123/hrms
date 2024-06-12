import fastapi as fa
from hrms.svc import attendance
import typing as ty
import pydantic as pyd
from datetime import datetime


class AttendanceLog(pyd.BaseModel):
    employee_id: int
    direction: bool
    time: datetime

router = fa.APIRouter()


@router.get("")
def list(attendance_svc: ty.Annotated[attendance.AttendanceLog, fa.Depends(attendance.AttendanceLog, use_cache=True)]):
    return attendance_svc.list()

@router.get("/{id}")
def get(id: int, attendance_svc: ty.Annotated[attendance.AttendanceLog, fa.Depends(attendance.AttendanceLog)]):
    return attendance_svc.get(id)

@router.post("")
def add(attendance_svc: ty.Annotated[attendance.AttendanceLog, fa.Depends(attendance.AttendanceLog)], attendance_data: AttendanceLog):
    return attendance_svc.add(attendance_data)

@router.put("/{id}")
def edit(id: int, employee_svc: ty.Annotated[attendance.AttendanceLog, fa.Depends(attendance.AttendanceLog)], attendance_data: AttendanceLog):
    return employee_svc.edit(id, attendance_data)

@router.delete("/{id}")
def remove(id: int, attendance_svc: ty.Annotated[attendance.AttendanceLog, fa.Depends(attendance.AttendanceLog)]):
    return attendance_svc.remove(id)