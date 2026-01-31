import logging
from tortoise import Tortoise

from app.use_cases.consultar_geral_use_case import ConsultarGeralUseCase
from app.database.config import init

logger = logging.getLogger(__name__)

async def get_empresas_filiais():
    return [
        {"codigo_empresa": 10, "codigo_filial": 1001},
        {"codigo_empresa": 10, "codigo_filial": 1005},
        {"codigo_empresa": 20, "codigo_filial": 2001},
        {"codigo_empresa": 40, "codigo_filial": 4001},
    ]


async def executar_consulta_por_empresa_filial(request: dict):
    empresa = request["codigo_empresa"]
    filial = request["codigo_filial"]

    logger.info(f"================ INÍCIO =================")

    use_case = ConsultarGeralUseCase(request)
    result = await use_case.execute()

    status = result.get("status")
    total = result.get("total", 0)

    logger.info(f"================ FIM =================\n")

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
