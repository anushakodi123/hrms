import fastapi as fa

router = fa.APIRouter()

@router.get("")
def pong():
    return "pong"