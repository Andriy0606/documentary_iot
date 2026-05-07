from abc import ABC, abstractmethod

class IEmployeeRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def get_by_id(self, employee_id: int):
        pass

    @abstractmethod
    def save(self, employee):
        pass

    @abstractmethod
    def update(self, employee_id: int, **fields):
        pass

    @abstractmethod
    def delete(self, employee_id: int) -> bool:
        pass

    @abstractmethod
    def read_csv(self, path):
        pass


class IEmployeeEquipmentRepository(ABC):
    @abstractmethod
    def list_by_employee(self, employee_id: int):
        pass

    @abstractmethod
    def save_many(self, equipment_items):
        """Persist a list of EmployeeEquipment items."""
        pass

    @abstractmethod
    def delete_by_employee(self, employee_id: int) -> int:
        pass