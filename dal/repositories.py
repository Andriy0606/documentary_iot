import csv
from dal.interfaces import IEmployeeRepository, IEmployeeEquipmentRepository
from models.models import Employee, EmployeeEquipment

class EmployeeRepository(IEmployeeRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def list(self):
        with self.session_factory() as session:
            return session.query(Employee).order_by(Employee.id.asc()).all()

    def get_by_id(self, employee_id: int):
        with self.session_factory() as session:
            return session.query(Employee).filter(Employee.id == employee_id).first()

    def read_csv(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) 
            return [row for row in reader if row]

    def save(self, employee):
        with self.session_factory() as session:
            session.add(employee)
            session.commit()
            session.refresh(employee)
            return employee

    def update(self, employee_id: int, **fields):
        with self.session_factory() as session:
            employee = session.query(Employee).filter(Employee.id == employee_id).first()
            if not employee:
                return None
            for k, v in fields.items():
                if v is not None and hasattr(employee, k):
                    setattr(employee, k, v)
            session.add(employee)
            session.commit()
            session.refresh(employee)
            return employee

    def delete(self, employee_id: int) -> bool:
        with self.session_factory() as session:
            employee = session.query(Employee).filter(Employee.id == employee_id).first()
            if not employee:
                return False
            session.delete(employee)
            session.commit()
            return True


class EmployeeEquipmentRepository(IEmployeeEquipmentRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def list_by_employee(self, employee_id: int):
        with self.session_factory() as session:
            return (
                session.query(EmployeeEquipment)
                .filter(EmployeeEquipment.employee_id == employee_id)
                .order_by(EmployeeEquipment.id.asc())
                .all()
            )

    def save_many(self, equipment_items):
        if not equipment_items:
            return []
        with self.session_factory() as session:
            session.add_all(equipment_items)
            session.commit()
            for item in equipment_items:
                session.refresh(item)
            return equipment_items

    def delete_by_employee(self, employee_id: int) -> int:
        with self.session_factory() as session:
            deleted = (
                session.query(EmployeeEquipment)
                .filter(EmployeeEquipment.employee_id == employee_id)
                .delete()
            )
            session.commit()
            return int(deleted or 0)