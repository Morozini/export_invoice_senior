import logging
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

from app.core.executor import run_consulta

if __name__ == "__main__":
    asyncio.run(run_consulta())
