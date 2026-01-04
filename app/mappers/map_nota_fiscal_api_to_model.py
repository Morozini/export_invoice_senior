
def map_nota_fiscal_api_to_model(nota_api: dict) -> dict:
    # pega campos customizados do usuário
    campo_usuario = {c["campo"]: c["valor"] for c in nota_api.get("campoUsuario", [])}

    # pega a data da primeira parcela, se existir
    data_vencimento_parcela = None
    if nota_api.get("parcela"):
        data_vencimento_parcela = nota_api["parcela"][0].get("vctPar")

    return {
        "codigo_empresa": nota_api.get("codEmp"),
        "codigo_filial": nota_api.get("codFil"),
        "codigo_fornecedor": nota_api.get("codFor"),
        "codigo_serie": nota_api.get("codSnf"),
        "numero_nota_fiscal": nota_api.get("numNfc"),
        "numero_ordem_compra": nota_api.get("numOcp") or None,
        "numero_titulo": nota_api.get("numTit") or None,
        "situacao_nota": nota_api.get("sitNfc") or "N/A",
        "codigo_forma_pagamento": nota_api.get("codFpg") or None,
        "data_emissao": nota_api.get("datEmi"),
        "data_entrada": nota_api.get("datEnt"),
        "data_fechamento_nf": nota_api.get("datFec"),
        "data_vencimento_parcela": data_vencimento_parcela,
        "observacao": nota_api.get("obsNfc") or " ",
        "valor_base": nota_api.get("vlrBru") or 0,
        "valor_liquido": nota_api.get("vlrLiq") or 0,
        "valor_diferenca": nota_api.get("vlrDar") or 0,
        "codigo_acumulador": campo_usuario.get("USU_CODACU"),
        "iss_vlr_retido": nota_api.get("vlrIss"),
        "ir_vlr_retido": nota_api.get("vlrIrf"),
        "inss_vlr_retido": nota_api.get("vlrIns"),
        "cofins_vlr_retido": nota_api.get("vlrCrt"),
        "pis_vlr_retido": nota_api.get("vlrPit"),
        "csll_vlr_retido": nota_api.get("vlrCsl"),
    }