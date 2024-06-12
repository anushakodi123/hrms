import fastapi as fa
from hrms.api import holiday, ping, employee, attendance,leave
from hrms.graphql import schema


app = fa.FastAPI()

app.include_router(ping.router, prefix="/ping")
app.include_router(employee.router, prefix="/employee")
app.include_router(attendance.router, prefix="/attendance")
app.include_router(leave.router, prefix="/leave")
app.include_router(holiday.router, prefix="/holiday")
app.include_router(schema.router, prefix="/graphql")
