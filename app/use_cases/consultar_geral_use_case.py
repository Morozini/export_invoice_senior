import logging
from datetime import datetime
from zeep.helpers import serialize_object

from app.repository.nota_fiscal_entrada_repository import NotaFiscalEntradaRepository
from app.services.get_consulta_geral_senior import GetConsultaGeralService
from app.mappers.create_consultageral_mappper import CreateNotaFiscalEntradaMapper
from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO

logger = logging.getLogger(__name__)


class ConsultarGeralUseCase:
    def __init__(self, request: dict):
        self.request = request
        self.service = GetConsultaGeralService()
        self.repository = NotaFiscalEntradaRepository()

    def _parse_date(self, date_str: str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            logger.warning(f"Data inválida: {date_str}")
            return None

    def _get_numero_ordem_compra(self, nota: dict):
        if nota.get("servico"):
            for serv in nota["servico"]:
                num_ocp = serv.get("numOcp")
                if num_ocp and str(num_ocp) != "0":
                    return num_ocp

        if nota.get("produto"):
            for prod in nota["produto"]:
                num_ocp = prod.get("numOcp")
                if num_ocp and str(num_ocp) != "0":
                    return num_ocp

        num_ocp = nota.get("numOcp")
        if num_ocp and str(num_ocp) != "0":
            return num_ocp

        return None

    def _get_numero_titulo(self, nota: dict):
        if nota.get("parcela"):
            return nota["parcela"][0].get("numTit")
        return None

    def _get_data_vencimento(self, nota: dict):
        if nota.get("parcela"):
            return self._parse_date(nota["parcela"][0].get("vctPar"))
        return None
    
    def _map_nota(self, nota: dict) -> dict:
        campo_usuario = {c["campo"]: c["valor"] for c in nota.get("campoUsuario", [])}

        codigo_empresa = nota.get("codEmp") or self.request.get("codigo_empresa")
        codigo_filial = nota.get("codFil") or self.request.get("codigo_filial")

        numero_ordem_compra = self._get_numero_ordem_compra(nota)

        valor_base_produto = nota.get("vlrBpr") or 0
        valor_base_servico = nota.get("vlrBse") or 0

        valor_liquido = (
            nota.get("vlrLiq")
            or nota.get("vlrliq")
            or 0
        )

        return {
            "codigo_empresa": int(codigo_empresa),
            "codigo_filial": int(codigo_filial),

            "codigo_fornecedor": nota.get("codFor"),
            "codigo_serie": nota.get("codSnf") or "SEM_SERIE",
            "numero_nota_fiscal": nota.get("numNfc"),

            "numero_ordem_compra": numero_ordem_compra,
            "numero_titulo": self._get_numero_titulo(nota),

            "situacao_nota": nota.get("sitNfc") or "N/A",
            "codigo_forma_pagamento": nota.get("codFpg") or None,

            "data_emissao": self._parse_date(nota.get("datEmi")),
            "data_entrada": self._parse_date(nota.get("datEnt")),
            "data_fechamento_nf": self._parse_date(nota.get("datFec")),
            "data_vencimento_parcela": self._get_data_vencimento(nota),

            "observacao": nota.get("obsNfc") or " ",

            "valor_base_produto": valor_base_produto,
            "valor_base_servico": valor_base_servico,
            "valor_liquido": valor_liquido,
            "valor_diferenca": nota.get("vlrDar") or 0,

            "codigo_acumulador": campo_usuario.get("USU_CODACU"),

            "iss_vlr_retido": nota.get("vlrIss"),
            "ir_vlr_retido": nota.get("vlrIrf"),
            "inss_vlr_retido": nota.get("vlrIns"),
            "cofins_vlr_retido": nota.get("vlrCrt"),
            "pis_vlr_retido": nota.get("vlrPit"),
            "csll_vlr_retido": nota.get("vlrCsl"),
        }

    async def execute(self) -> dict:
        try:
            dto = GetConsultaGeralSeniorDTO(**self.request)

            indice_pagina = 1
            total_processado = 0

            logger.info(
                f"Iniciando paginação | Empresa {dto.codigo_empresa} | Filial {dto.codigo_filial}"
            )

            while True:
                logger.info(f"Consultando página {indice_pagina}")

                payload = CreateNotaFiscalEntradaMapper.create(
                    dto,
                    indice_pagina=indice_pagina
                )

                response = self.service.get_nota_fiscal_entrada(payload)

                if not response:
                    logger.info(f"Sem resposta da API na página {indice_pagina}. Encerrando.")
                    break

                response = serialize_object(response)
                notas = response.get("notaFiscal", [])

                if not notas:
                    logger.info(
                        f"Nenhuma nota retornada na página {indice_pagina}. Fim da paginação."
                    )
                    break

                notas_mapeadas = []

                for nota in notas:
                    if not nota:
                        continue

                    try:
                        nota_map = self._map_nota(nota)
                        notas_mapeadas.append(nota_map)
                    except Exception as e:
                        logger.error(
                            f"Erro ao mapear nota numNfc={nota.get('numNfc')} | Erro: {e}",
                            exc_info=True
                        )

                if notas_mapeadas:
                    await self.repository.bulk_upsert(notas_mapeadas)
                    logger.info(
                        f"{len(notas_mapeadas)} notas processadas na página {indice_pagina}."
                    )
                    total_processado += len(notas_mapeadas)

                indice_pagina += 1

            logger.info(
                f"Processo finalizado | Empresa {dto.codigo_empresa} | Filial {dto.codigo_filial} | Total: {total_processado}"
            )

            return {
                "status": "ok",
                "total": total_processado
            }

        except Exception as e:
            logger.error(f"Erro no processamento das notas: {e}", exc_info=True)
            return {
                "status": "error",
                "total": 0,
                "message": str(e)
            }
