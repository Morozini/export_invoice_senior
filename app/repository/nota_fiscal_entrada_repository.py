from app.database.models import NotasFiscalEntradaApiSenior

class NotaFiscalEntradaRepository:

    @staticmethod
    async def bulk_save(data_list: list[dict]):
        """
        Salva notas já mapeadas pelo UseCase diretamente no banco
        """
        objects = [NotasFiscalEntradaApiSenior(**nota) for nota in data_list]
        await NotasFiscalEntradaApiSenior.bulk_create(objects)
