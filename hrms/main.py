import fastapi as fa
from hrms.api import ping, employee

app = fa.FastAPI()

app.include_router(ping.router, prefix="/ping")
app.include_router(employee.router, prefix="/employee")
