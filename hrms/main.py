import fastapi as fa
from hrms.api import ping, employee
from hrms.graphql import employeee, sample


app = fa.FastAPI()

app.include_router(ping.router, prefix="/ping")
app.include_router(employee.router, prefix="/employee")
app.include_router(sample.graphql_app, prefix="/graphql")
app.include_router(employeee.graphql_schema2, prefix="/graphql1")
