from tortoise import fields
from tortoise.models import Model


class NotasFiscalEntradaApiSenior(Model):
    id = fields.IntField(pk=True)

    codigo_empresa = fields.IntField(description="codEmp")
    codigo_filial = fields.IntField(description="codFil")
    codigo_fornecedor = fields.IntField(description="codFor")
    codigo_serie = fields.CharField(max_length=10, default="SEM_SERIE", description="codSnf")
    numero_nota_fiscal = fields.IntField(description="numNfc")
    numero_ordem_compra = fields.IntField(null=True, description="numOcp")
    numero_titulo = fields.CharField(max_length=20, null=True, description="numTit")
    situacao_nota = fields.CharField(max_length=20, description="sitNfc")
    codigo_forma_pagamento = fields.IntField(null=True, description="codFpg")
    data_emissao = fields.DateField(description="datEmi")
    data_entrada = fields.DateField(description="datEnt")
    data_fechamento_nf = fields.DateField(null=True, description="datFec")
    data_vencimento_parcela = fields.DateField(null=True, description="vctPar")
    observacao = fields.TextField(null=True, description="obsNfc")
    valor_base_servico = fields.FloatField(max_digits=15, description="vlrBse")
    valor_base_produto = fields.FloatField(max_digits=15, description="vlrBpr")
    valor_liquido = fields.FloatField(max_digits=15, description="vlrLiq")
    valor_diferenca = fields.FloatField(max_digits=15, description="vlrDar")
    codigo_acumulador = fields.CharField(max_length=20, null=True, description="USU_CodAcu")
    iss_vlr_retido = fields.FloatField(max_digits=15, null=True, description="vlrIss")
    ir_vlr_retido = fields.FloatField(max_digits=15, null=True, description="vlrIrf")
    inss_vlr_retido = fields.FloatField(max_digits=15, null=True, description="vlrIns")
    cofins_vlr_retido = fields.FloatField(max_digits=15, null=True, description="vlrCrt")
    pis_vlr_retido = fields.FloatField(max_digits=15, null=True, description="vlrPit")
    csll_vlr_retido = fields.FloatField(max_digits=15, null=True, description="vlrCsl")
    class Meta:
        table = "task_notas_fiscal_entrada_api_senior"
        unique_together = (
            "codigo_filial",
            "codigo_fornecedor",
            "numero_nota_fiscal",
        )

class RateioNotasFiscalEntradaApiSenior(Model):

    id = fields.IntField(pk=True)
    nota_fiscal_entrada = fields.ForeignKeyField(
        "models.NotasFiscalEntradaApiSenior",
        related_name="rateios",
        on_delete=fields.CASCADE,
    )
    codigo_empresa = fields.IntField(description="codEmp")
    codigo_filial = fields.IntField(description="codFil")
    codigo_centro_custo = fields.CharField(max_length=20, null=True, description="codCcu")
    valor_rateio_centro_custo = fields.FloatField(max_digits=15, null=True, description="vlrRat")
    codigo_fase_projeto = fields.CharField(max_length=20, null=True, description="codFpj")
    codigo_conta_financeira = fields.CharField(max_length=20, null=True, description="ctaFin")
    valor_rateio_conta_financeira = fields.FloatField(max_digits=15, null=True, description="vlrCta")
    codigo_projeto = fields.CharField(max_length=20, null=True, description="numPrj")
    
    class Meta:
        table = "task_rateio_notas_fiscal_entrada_api_senior"