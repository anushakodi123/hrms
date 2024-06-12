from datetime import datetime
import fastapi as fa
from hrms.svc import holiday
import typing as ty
import pydantic as pyd


class Holiday(pyd.BaseModel):
    name: str
    on: datetime

router = fa.APIRouter()


@router.get("")
def list(holiday_svc: ty.Annotated[holiday.Holiday, fa.Depends(holiday.Holiday, use_cache=True)]):
    return holiday_svc.list()

@router.get("/{id}")
def get(id: int, holiday_svc: ty.Annotated[holiday.Holiday, fa.Depends(holiday.Holiday)]):
    return holiday_svc.get(id)

@router.post("")
def add(holiday_svc: ty.Annotated[holiday.Holiday, fa.Depends(holiday.Holiday)], holiday: Holiday):
    return holiday_svc.add(holiday)

@router.put("/{id}")
def edit(id: int, holiday_svc: ty.Annotated[holiday.Holiday, fa.Depends(holiday.Holiday)], holiday: Holiday):
    return holiday_svc.edit(id, holiday)

@router.delete("/{id}")
def remove(id: int, holiday_svc: ty.Annotated[holiday.Holiday, fa.Depends(holiday.Holiday)]):
    return holiday_svc.remove(id)