import asyncio
import logging
from app.celery import celery_app
from app.core.executor import run_consulta

logger = logging.getLogger(__name__)

@celery_app.task(name="executar_task_nota_fiscal_entrada")
def executar_task_nota_fiscal_entrada():
    try:
        logger.info("Iniciando execução da task de nota fiscal entrada...")
        asyncio.run(run_consulta())
        logger.info("Execução concluída com sucesso.")
        return {"status": "success", "message": "Consulta finalizada com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao executar a task: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}
