from app.database.models import NotasFiscalEntradaApiSenior


class NotaFiscalEntradaRepository:

    async def bulk_upsert(self, notas: list[dict]) -> int:
        if not notas:
            return 0

        objetos = [
            NotasFiscalEntradaApiSenior(**nota)
            for nota in notas
        ]

        await NotasFiscalEntradaApiSenior.bulk_create(
            objetos,
            ignore_conflicts=True
        )

        return len(objetos)
