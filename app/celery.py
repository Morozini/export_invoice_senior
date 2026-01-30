from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "app",
    broker=f"amqp://admin:admin@rabbitmq:5672//",
)

celery_app.autodiscover_tasks(["app"])

celery_app.conf.task_default_queue = "projeto_notas_fiscais_entrada"

celery_app.conf.task_acks_late = True
celery_app.conf.timezone = "America/Sao_Paulo" # type: ignore
celery_app.conf.enable_utc = False

celery_app.conf.beat_schedule = {
    "execute_task_nota_fiscal_entrada": {
        "task": "executar_task_nota_fiscal_entrada",
        "schedule": crontab(hour=[7, 12, 17], minute=0),
    },
}
