
from app.database.models import NotasFiscalEntradaApiSenior


class NotaFiscalEntradaRepository:

    async def bulk_upsert(self, notas: list[dict]):
        for nota in notas:
            await NotasFiscalEntradaApiSenior.update_or_create(
                defaults=nota,
                codigo_empresa=nota["codigo_empresa"],
                codigo_filial=nota["codigo_filial"],
                codigo_serie=nota["codigo_serie"],
                numero_nota_fiscal=nota["numero_nota_fiscal"],
            )
