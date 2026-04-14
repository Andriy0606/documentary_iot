from models.models import Employee, EmployeeEquipment

class EmployeeService:
    def __init__(self, employee_repo, equipment_repo):
        self.employee_repo = employee_repo
        self.equipment_repo = equipment_repo

    def list_employees(self):
        return self.employee_repo.list()

    def get_employee(self, employee_id: int):
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            return None
        equipment = self.equipment_repo.list_by_employee(employee_id)
        return {"employee": employee, "equipment": equipment}

    def create_employee(
        self,
        full_name: str,
        email: str,
        start_date: str,
        position: str,
        status: str = "NEW",
        equipment_names: list[str] | None = None,
    ):
        employee = Employee(
            full_name=(full_name or "").strip(),
            email=(email or "").strip(),
            start_date=(start_date or "").strip(),
            position=(position or "").strip(),
            status=(status or "NEW").strip() or "NEW",
        )
        saved_employee = self.employee_repo.save(employee)

        equipment_items: list[EmployeeEquipment] = []
        if equipment_names:
            equipment_items = [
                EmployeeEquipment(employee_id=saved_employee.id, name=name.strip())
                for name in equipment_names
                if name and name.strip()
            ]
        self.equipment_repo.save_many(equipment_items)
        return saved_employee

    def update_employee(
        self,
        employee_id: int,
        *,
        full_name: str | None = None,
        email: str | None = None,
        start_date: str | None = None,
        position: str | None = None,
        status: str | None = None,
        equipment_names: list[str] | None = None,
    ):
        fields = {}
        if full_name is not None:
            fields["full_name"] = full_name.strip()
        if email is not None:
            fields["email"] = email.strip()
        if start_date is not None:
            fields["start_date"] = start_date.strip()
        if position is not None:
            fields["position"] = position.strip()
        if status is not None:
            fields["status"] = (status.strip() or "NEW")

        employee = self.employee_repo.update(employee_id, **fields)
        if not employee:
            return None

        if equipment_names is not None:
            self.equipment_repo.delete_by_employee(employee_id)
            equipment_items = [
                EmployeeEquipment(employee_id=employee_id, name=name.strip())
                for name in equipment_names
                if name and name.strip()
            ]
            self.equipment_repo.save_many(equipment_items)

        return employee

    def delete_employee(self, employee_id: int) -> bool:
        self.equipment_repo.delete_by_employee(employee_id)
        return self.employee_repo.delete(employee_id)

    def process_csv(self, path: str):
        rows = self.employee_repo.read_csv(path)
        with self.employee_repo.session_factory() as session:
            session.query(EmployeeEquipment).delete()
            session.query(Employee).delete()
            session.commit()

        for row in rows:
            # CSV: full_name,email,start_date,position,status,equipment,department
            full_name = (row[0] or "").strip()
            email = (row[1] or "").strip()
            start_date = (row[2] or "").strip()
            position = (row[3] or "").strip()
            status = (row[4] or "").strip() or "NEW"
            equipment_raw = (row[5] or "").strip() if len(row) > 5 else ""

            employee = Employee(
                full_name=full_name,
                email=email,
                start_date=start_date,
                position=position,
                status=status or "NEW",
            )
            saved_employee = self.employee_repo.save(employee)

            equipment_items = []
            if equipment_raw:
                equipment_names = [p.strip() for p in equipment_raw.split(";") if p.strip()]
                equipment_items = [
                    EmployeeEquipment(employee_id=saved_employee.id, name=name)
                    for name in equipment_names
                ]
            self.equipment_repo.save_many(equipment_items)

        return True