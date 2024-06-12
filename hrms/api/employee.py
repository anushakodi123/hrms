import fastapi as fa
from hrms.svc import employee
import typing as ty
import pydantic as pyd


class Employee(pyd.BaseModel):
    name: str
    designation: str
    reports_to: int | None
    project: str

router = fa.APIRouter()


@router.get("")
def list(employee_svc: ty.Annotated[employee.Employee, fa.Depends(employee.Employee, use_cache=True)]):
    return employee_svc.list()

@router.get("/{id}")
def get(id: int, employee_svc: ty.Annotated[employee.Employee, fa.Depends(employee.Employee)]):
    return employee_svc.get(id)

@router.post("")
def add(employee_svc: ty.Annotated[employee.Employee, fa.Depends(employee.Employee)], employee: Employee):
    return employee_svc.add(employee)

@router.put("/{id}")
def edit(id: int, employee_svc: ty.Annotated[employee.Employee, fa.Depends(employee.Employee)], employee: Employee):
    return employee_svc.edit(id, employee)

@router.delete("/{id}")
def remove(id: int, employee_svc: ty.Annotated[employee.Employee, fa.Depends(employee.Employee)]):
    return employee_svc.remove(id)