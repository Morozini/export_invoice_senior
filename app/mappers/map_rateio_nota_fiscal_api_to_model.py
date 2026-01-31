def map_rateio_api_to_model(rateio_api: dict) -> dict:
    return {
        "codigo_empresa": rateio_api.get("codEmp"),
        "codigo_filial": rateio_api.get("codFil"),
        "codigo_centro_custo": rateio_api.get("codCcu"),
        "valor_rateio_centro_custo": rateio_api.get("vlrRat"),
        "codigo_fase_projeto": rateio_api.get("codFpj"),
        "codigo_conta_financeira": rateio_api.get("ctaFin"),
        "valor_rateio_conta_financeira": rateio_api.get("vlrCta"),
        "codigo_projeto": rateio_api.get("numPrj"),
    }
