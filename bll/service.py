from models.models import Employee, EmployeeEquipment

class EmployeeService:
    def __init__(self, employee_repo, equipment_repo):
        self.employee_repo = employee_repo
        self.equipment_repo = equipment_repo

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