import csv
from dal.interfaces import IEmployeeRepository, IEmployeeEquipmentRepository
from models.models import Employee, EmployeeEquipment

class EmployeeRepository(IEmployeeRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

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


class EmployeeEquipmentRepository(IEmployeeEquipmentRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def save_many(self, equipment_items):
        if not equipment_items:
            return []
        with self.session_factory() as session:
            session.add_all(equipment_items)
            session.commit()
            for item in equipment_items:
                session.refresh(item)
            return equipment_items