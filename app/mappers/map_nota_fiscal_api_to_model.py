

def map_nota_fiscal_api_to_model(nota_api: dict) -> dict:
    campo_usuario = {c["campo"]: c["valor"] for c in nota_api.get("campoUsuario", [])}

    parcela = nota_api.get("parcela") or []
    parcela_0 = parcela[0] if parcela else {}

    data_vencimento_parcela = parcela_0.get("vctPar")
    numero_titulo = parcela_0.get("numTit")

    if numero_titulo in ("", " ", 0, "0"):
        numero_titulo = None

    numero_ordem_compra = nota_api.get("numOcp")

    if nota_api.get("servico"):
        servico = nota_api["servico"][0]
        numero_ordem_compra = servico.get("numOcp") or numero_ordem_compra

    if nota_api.get("produto"):
        produto = nota_api["produto"][0]
        numero_ordem_compra = produto.get("numOcp") or numero_ordem_compra

    if numero_ordem_compra in (0, "0", "", " "):
        numero_ordem_compra = None

    valor_base_produto = nota_api.get("vlrBpr") or 0
    valor_base_servico = nota_api.get("vlrBse") or 0

    valor_liquido = (
        nota_api.get("vlrLiq")
        if nota_api.get("vlrLiq") not in (None, 0, 0.0, "0", "0.0")
        else nota_api.get("vlrliq")
        if nota_api.get("vlrliq") not in (None, 0, 0.0, "0", "0.0")
        else None
    )

    if not valor_liquido and nota_api.get("servico"):
        valor_liquido = nota_api["servico"][0].get("vlrLiq")

    valor_liquido = valor_liquido or 0

    return {
        "codigo_empresa": nota_api.get("codEmp"),
        "codigo_filial": nota_api.get("codFil"),
        "codigo_fornecedor": nota_api.get("codFor"),
        "codigo_serie": nota_api.get("codSnf"),
        "numero_nota_fiscal": nota_api.get("numNfc"),

        "numero_ordem_compra": numero_ordem_compra,
        "numero_titulo": numero_titulo,

        "situacao_nota": nota_api.get("sitNfc") or "N/A",
        "codigo_forma_pagamento": nota_api.get("codFpg") or None,

        "data_emissao": nota_api.get("datEmi"),
        "data_entrada": nota_api.get("datEnt"),
        "data_fechamento_nf": nota_api.get("datFec"),
        "data_vencimento_parcela": data_vencimento_parcela,

        "observacao": nota_api.get("obsNfc") or " ",

        "valor_base_produto": valor_base_produto,
        "valor_base_servico": valor_base_servico,
        "valor_liquido": valor_liquido,

        "valor_diferenca": nota_api.get("vlrDar") or 0,
        "codigo_acumulador": campo_usuario.get("USU_CODACU"),

        "iss_vlr_retido": nota_api.get("vlrIss"),
        "ir_vlr_retido": nota_api.get("vlrIrf"),
        "inss_vlr_retido": nota_api.get("vlrIns"),
        "cofins_vlr_retido": nota_api.get("vlrCrt"),
        "pis_vlr_retido": nota_api.get("vlrPit"),
        "csll_vlr_retido": nota_api.get("vlrCsl"),
    }
