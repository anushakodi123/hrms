
System Design for HRMS

Employee POV
    Show employee details – id, name, designation, reporting manager, project, tech stack, department
    Attendance tracking, Leaves, Calendar
    Search for other employees
    Salary components, salary slips, IT forms
    Ticketing system to raise requests for resources ie. git repos, enterprise tools, etc.

HR POV

You have many users that have different roles in this system

employee
    id int pk
    name text
    designation text
    department text
    reports_to employee.id
    project text


attendance
    id int pk
    employee_id employee.id
    direction IN/OUT
    time datetime

leave
    id int pk
    employee_id employee.id
    type SICK/CASUAL
    since datetime
    till datetime

holiday
    id int pk
    name text
    on date
