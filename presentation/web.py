from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from container import Container


router = APIRouter()
templates = Jinja2Templates(directory="templates")
container = Container()


def _parse_equipment(equipment_raw: str) -> list[str]:
    if not equipment_raw:
        return []
    return [p.strip() for p in equipment_raw.split(";") if p.strip()]


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse(url="/employees", status_code=303)


@router.get("/employees", response_class=HTMLResponse)
def employees_list(request: Request):
    srv = container.employee_service()
    employees = srv.list_employees()
    return templates.TemplateResponse(
        request,
        "employees/index.html",
        {"employees": employees},
    )


@router.get("/employees/create", response_class=HTMLResponse)
def employees_create_form(request: Request):
    return templates.TemplateResponse(request, "employees/create.html", {})


@router.post("/employees/create")
def employees_create(
    full_name: str = Form(""),
    email: str = Form(""),
    start_date: str = Form(""),
    position: str = Form(""),
    status: str = Form("NEW"),
    equipment: str = Form(""),
):
    srv = container.employee_service()
    srv.create_employee(
        full_name=full_name,
        email=email,
        start_date=start_date,
        position=position,
        status=status,
        equipment_names=_parse_equipment(equipment),
    )
    return RedirectResponse(url="/employees", status_code=303)


@router.get("/employees/{employee_id}", response_class=HTMLResponse)
def employees_details(request: Request, employee_id: int):
    srv = container.employee_service()
    data = srv.get_employee(employee_id)
    if not data:
        return RedirectResponse(url="/employees", status_code=303)
    return templates.TemplateResponse(
        request,
        "employees/details.html",
        {"employee": data["employee"], "equipment": data["equipment"]},
    )


@router.get("/employees/{employee_id}/edit", response_class=HTMLResponse)
def employees_edit_form(request: Request, employee_id: int):
    srv = container.employee_service()
    data = srv.get_employee(employee_id)
    if not data:
        return RedirectResponse(url="/employees", status_code=303)
    equipment_str = "; ".join([e.name for e in data["equipment"]])
    return templates.TemplateResponse(
        request,
        "employees/edit.html",
        {"employee": data["employee"], "equipment": equipment_str},
    )


@router.post("/employees/{employee_id}/edit")
def employees_edit(
    employee_id: int,
    full_name: str = Form(""),
    email: str = Form(""),
    start_date: str = Form(""),
    position: str = Form(""),
    status: str = Form("NEW"),
    equipment: str = Form(""),
):
    srv = container.employee_service()
    srv.update_employee(
        employee_id,
        full_name=full_name,
        email=email,
        start_date=start_date,
        position=position,
        status=status,
        equipment_names=_parse_equipment(equipment),
    )
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)


@router.post("/employees/{employee_id}/delete")
def employees_delete(employee_id: int):
    srv = container.employee_service()
    srv.delete_employee(employee_id)
    return RedirectResponse(url="/employees", status_code=303)

