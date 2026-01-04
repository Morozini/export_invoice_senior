import asyncio
import logging
from tortoise import Tortoise
from app.use_cases.consultar_geral_use_case import ConsultarGeralUseCase
from app.database.config import init  # sua função de inicialização do Tortoise

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    # Inicializa o ORM
    logger.info("Inicializando ORM (Tortoise)...")
    await init()
    logger.info("ORM inicializado com sucesso.")

    # Exemplo: uma empresa/filial só
    request = {
        "codigo_empresa": 10,
        "codigo_filial": 1001,
    }

    use_case = ConsultarGeralUseCase(request)
    resultado = await use_case.execute()

    logger.info(f"Resultado da execução: {resultado}")

    # Fecha conexões
    await Tortoise.close_connections()
    logger.info("Conexões encerradas.")

if __name__ == "__main__":
    asyncio.run(main())
