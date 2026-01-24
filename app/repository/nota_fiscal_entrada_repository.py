from app.database.models import NotasFiscalEntradaApiSenior


class NotaFiscalEntradaRepository:

    async def bulk_upsert(self, notas: list[dict]):
        if not notas:
            return

        objs = [NotasFiscalEntradaApiSenior(**nota) for nota in notas]

        await NotasFiscalEntradaApiSenior.bulk_create(
            objs,
            ignore_conflicts=True
        )
