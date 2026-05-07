import os

from dependency_injector import containers, providers
from dal.database import SessionLocal
from dal.repositories import EmployeeRepository, EmployeeEquipmentRepository
from bll.service import EmployeeService
from outputs.console import ConsoleOutputStrategy
from outputs.kafka import KafkaOutputStrategy

class Container(containers.DeclarativeContainer):
    # Використовуємо Object, щоб передати сам клас SessionLocal як фабрику
    db_session = providers.Object(SessionLocal) 

    employee_repo = providers.Factory(EmployeeRepository, session_factory=db_session)
    equipment_repo = providers.Factory(EmployeeEquipmentRepository, session_factory=db_session)

    output_strategy = providers.Selector(
        providers.Callable(lambda: os.getenv("OUTPUT_SINK", "console").strip().lower() or "console"),
        console=providers.Singleton(ConsoleOutputStrategy),
        kafka=providers.Singleton(
            KafkaOutputStrategy,
            bootstrap_servers=providers.Callable(
                lambda: os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
            ),
            topic=providers.Callable(lambda: os.getenv("KAFKA_TOPIC", "employees_import_log")),
        ),
    )

    employee_service = providers.Factory(
        EmployeeService,
        employee_repo=employee_repo,
        equipment_repo=equipment_repo,
        output=output_strategy,
    )