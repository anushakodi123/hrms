import fastapi as fa
from hrms.svc import employee
import typing as ty

router = fa.APIRouter()


@router.get("")
def list(employee_svc: ty.Annotated[employee.Employee, fa.Depends(employee.Employee)]):
    return employee_svc.list()

@router.get("/{id}")
def view(id: str):
    return {"employee": id}