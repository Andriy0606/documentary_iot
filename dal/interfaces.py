from abc import ABC, abstractmethod

class IEmployeeRepository(ABC):
    @abstractmethod
    def save(self, employee):
        pass

    @abstractmethod
    def read_csv(self, path):
        pass


class IEmployeeEquipmentRepository(ABC):
    @abstractmethod
    def save_many(self, equipment_items):
        """Persist a list of EmployeeEquipment items."""
        pass