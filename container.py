from dependency_injector import containers, providers
from dal.database import SessionLocal
from dal.repositories import EmployeeRepository, EmployeeEquipmentRepository
from bll.service import EmployeeService

class Container(containers.DeclarativeContainer):
    # Використовуємо Object, щоб передати сам клас SessionLocal як фабрику
    db_session = providers.Object(SessionLocal) 

    employee_repo = providers.Factory(EmployeeRepository, session_factory=db_session)
    equipment_repo = providers.Factory(EmployeeEquipmentRepository, session_factory=db_session)

    employee_service = providers.Factory(
        EmployeeService,
        employee_repo=employee_repo,
        equipment_repo=equipment_repo,
    )