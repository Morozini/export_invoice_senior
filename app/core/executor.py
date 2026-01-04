import logging
from tortoise import Tortoise

from app.use_cases.consultar_geral_use_case import ConsultarGeralUseCase
from app.database.config import init

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

async def get_empresas_filiais():
    return [
        {"codigo_empresa": 10, "codigo_filial": 1001},
        {"codigo_empresa": 10, "codigo_filial": 1005},
        {"codigo_empresa": 20, "codigo_filial": 2001},
        {"codigo_empresa": 40, "codigo_filial": 4001},
    ]

async def executar_consulta_por_empresa_filial(request: dict):
    logger.info(
        f"Iniciando consulta | Empresa {request['codigo_empresa']} | "
        f"Filial {request['codigo_filial']}"
    )

    use_case = ConsultarGeralUseCase(request)
    result = await use_case.execute()

    logger.info(
        f"Finalizado | Empresa {request['codigo_empresa']} | "
        f"Filial {request['codigo_filial']} | "
        f"Total OC: {result.get('total', 0)}"
    )


async def run_consulta(empresas_filiais=None):
    try:
        logger.info("Inicializando ORM (Tortoise)...")
        await init()
        logger.info("ORM inicializado com sucesso.")

        if not empresas_filiais:
            empresas_filiais = await get_empresas_filiais()

        for request in empresas_filiais:
            try:
                await executar_consulta_por_empresa_filial(request)
            except Exception as e:
                logger.error(
                    f"Erro Empresa {request['codigo_empresa']} | "
                    f"Filial {request['codigo_filial']}: {e}",
                    exc_info=True
                )

    finally:
        logger.info("Encerrando conexões com o banco...")
        await Tortoise.close_connections()
        logger.info("Conexões encerradas.")
