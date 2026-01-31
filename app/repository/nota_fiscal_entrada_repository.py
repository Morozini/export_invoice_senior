from app.database.models import NotasFiscalEntradaApiSenior


class NotaFiscalEntradaRepository:

    async def bulk_upsert(self, notas: list[dict]) -> list[NotasFiscalEntradaApiSenior]:
        if not notas:
            return []

        await NotasFiscalEntradaApiSenior.bulk_create(
            [NotasFiscalEntradaApiSenior(**nota) for nota in notas],
            ignore_conflicts=True
        )

        # 🔑 BUSCAR DO BANCO (AGORA COM ID)
        filtros = [
            (
                nota["codigo_filial"],
                nota["codigo_fornecedor"],
                nota["numero_nota_fiscal"],
            )
            for nota in notas
        ]

        notas_salvas = await NotasFiscalEntradaApiSenior.filter(
            codigo_filial__in=[f[0] for f in filtros],
            codigo_fornecedor__in=[f[1] for f in filtros],
            numero_nota_fiscal__in=[f[2] for f in filtros],
        )

        return list(notas_salvas)
