from datetime import datetime
import fastapi as fa
from hrms.svc import leave
import typing as ty
import pydantic as pyd


class Leave(pyd.BaseModel):
    employee_id: int
    type: str
    time: datetime

router = fa.APIRouter()


@router.get("")
def list(leave_svc: ty.Annotated[leave.Leave, fa.Depends(leave.Leave, use_cache=True)]):
    return leave_svc.list()

@router.get("/{id}")
def get(id: int, leave_svc: ty.Annotated[leave.Leave, fa.Depends(leave.Leave)]):
    return leave_svc.get(id)

@router.post("")
def add(leave_svc: ty.Annotated[leave.Leave, fa.Depends(leave.Leave)], leave: Leave):
    return leave_svc.add(leave)

@router.put("/{id}")
def edit(id: int, leave_svc: ty.Annotated[leave.Leave, fa.Depends(leave.Leave)], leave: Leave):
    return leave_svc.edit(id, leave)

@router.delete("/{id}")
def remove(id: int, leave_svc: ty.Annotated[leave.Leave, fa.Depends(leave.Leave)]):
    return leave_svc.remove(id)