from app.database.models import RateioNotasFiscalEntradaApiSenior


class RateioNotaFiscalEntradaRepository:

    async def bulk_upsert(self, rateios: list[dict]) -> int:
        if not rateios:
            return 0

        total = 0

        for rateio in rateios:
            await RateioNotasFiscalEntradaApiSenior.update_or_create(
                # 🔑 CHAVE DO RATEIO
                nota_fiscal_entrada=rateio["nota_fiscal_entrada"],
                codigo_centro_custo=rateio.get("codigo_centro_custo"),
                codigo_conta_financeira=rateio.get("codigo_conta_financeira"),
                codigo_projeto=rateio.get("codigo_projeto"),
                codigo_fase_projeto=rateio.get("codigo_fase_projeto"),

                # 🔄 TODOS OS CAMPOS ATUALIZÁVEIS
                defaults={
                    "codigo_empresa": rateio.get("codigo_empresa"),
                    "codigo_filial": rateio.get("codigo_filial"),
                    "valor_rateio_centro_custo": rateio.get("valor_rateio_centro_custo"),
                    "valor_rateio_conta_financeira": rateio.get("valor_rateio_conta_financeira"),
                },
            )
            total += 1

        return total
