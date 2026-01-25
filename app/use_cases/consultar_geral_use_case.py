import logging
from datetime import date, datetime
from zeep.helpers import serialize_object

from app.repository.nota_fiscal_entrada_repository import NotaFiscalEntradaRepository
from app.services.get_consulta_geral_senior import GetConsultaGeralService
from app.mappers.create_consultageral_mappper import CreateNotaFiscalEntradaMapper
from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO
from app.utils.gerar_semanas import gerar_semanas

logger = logging.getLogger(__name__)


class ConsultarGeralUseCase:
    LIMITE_PAGINA = 50

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
        for grupo in ("servico", "produto"):
            if nota.get(grupo):
                for item in nota[grupo]:
                    num_ocp = item.get("numOcp")
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
        campo_usuario = {
            c["campo"]: c["valor"]
            for c in nota.get("campoUsuario", [])
        }

        return {
            "codigo_empresa": int(nota.get("codEmp") or self.request["codigo_empresa"]),
            "codigo_filial": int(nota.get("codFil") or self.request["codigo_filial"]),

            "codigo_fornecedor": nota.get("codFor"),
            "codigo_serie": nota.get("codSnf") or "SEM_SERIE",
            "numero_nota_fiscal": nota.get("numNfc"),

            "numero_ordem_compra": self._get_numero_ordem_compra(nota),
            "numero_titulo": self._get_numero_titulo(nota),

            "situacao_nota": nota.get("sitNfc") or "N/A",
            "codigo_forma_pagamento": nota.get("codFpg"),

            "data_emissao": self._parse_date(nota.get("datEmi")),
            "data_entrada": self._parse_date(nota.get("datEnt")),
            "data_fechamento_nf": self._parse_date(nota.get("datFec")),
            "data_vencimento_parcela": self._get_data_vencimento(nota),

            "observacao": nota.get("obsNfc") or " ",

            "valor_base_produto": nota.get("vlrBpr") or 0,
            "valor_base_servico": nota.get("vlrBse") or 0,
            "valor_liquido": nota.get("vlrLiq") or nota.get("vlrliq") or 0,
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

            data_inicio = date(2026, 1, 1)
            data_fim = date(2026, 12, 31)

            total_processado = 0

            logger.info(
                f"Iniciando consulta | Empresa {dto.codigo_empresa} | Filial {dto.codigo_filial}"
            )

            for ini, fim in gerar_semanas(data_inicio, data_fim):
                indice_pagina = 1

                logger.info(
                    f"Período {ini:%d/%m/%Y} → {fim:%d/%m/%Y}"
                )

                while True:
                    payload = CreateNotaFiscalEntradaMapper.create(
                        dto=dto,
                        dat_ini=ini.strftime("%d/%m/%Y"),
                        dat_fim=fim.strftime("%d/%m/%Y"),
                        indice_pagina=indice_pagina,
                        limite_pagina=self.LIMITE_PAGINA,
                    )

                    response = self.service.get_nota_fiscal_entrada(payload)
                    if not response:
                        break

                    response = serialize_object(response)
                    notas = response.get("notaFiscal", [])

                    if not notas:
                        break

                    notas_mapeadas = []

                    for nota in notas:
                        try:
                            notas_mapeadas.append(self._map_nota(nota))
                        except Exception as e:
                            logger.error(
                                f"Erro ao mapear NF {nota.get('numNfc')}: {e}",
                                exc_info=True,
                            )

                    if notas_mapeadas:
                        await self.repository.bulk_upsert(notas_mapeadas)
                        total_processado += len(notas_mapeadas)

                    if len(notas) < self.LIMITE_PAGINA:
                        break

                    indice_pagina += 1

            logger.info(
                f"Finalizado | Empresa {dto.codigo_empresa} | "
                f"Filial {dto.codigo_filial} | Total {total_processado}"
            )

            return {"status": "ok", "total": total_processado}

        except Exception as e:
            logger.error("Erro no processamento", exc_info=True)
            return {"status": "error", "total": 0, "message": str(e)}
