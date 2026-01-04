import logging
from datetime import datetime
from app.repository.nota_fiscal_entrada_repository import NotaFiscalEntradaRepository
from app.services.get_consulta_geral_senior import GetConsultaGeralService
from app.mappers.create_consultageral_mappper import CreateNotaFiscalEntradaMapper
from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO
from zeep.helpers import serialize_object

logger = logging.getLogger(__name__)


class ConsultarGeralUseCase:
    def __init__(self, request: dict):
        """
        request: dict com 'codigo_empresa' e 'codigo_filial'
        """
        self.request = request
        self.service = GetConsultaGeralService()
        self.repository = NotaFiscalEntradaRepository()

    def _parse_date(self, date_str: str):
        """Converte string no formato dd/mm/yyyy para datetime.date"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            logger.warning(f"Data inválida: {date_str}")
            return None

    def _map_nota(self, nota: dict) -> dict:
        """
        Mapeia a nota da API para o modelo do banco, usando valores do request
        caso a API não retorne 'codEmp' ou 'codFil'.
        """
        campo_usuario = {c["campo"]: c["valor"] for c in nota.get("campoUsuario", [])}

        codigo_empresa = nota.get("codEmp") or self.request["codigo_empresa"]
        codigo_filial = nota.get("codFil") or self.request["codigo_filial"]

        if codigo_empresa is None or codigo_filial is None:
            logger.warning(f"Nota ignorada por falta de campos obrigatórios: {nota}")
            return None

        return {
            "codigo_empresa": nota.get("codEmp"),
            "codigo_filial": nota.get("codFil"),
            "codigo_fornecedor": nota.get("codFor"),
            "codigo_serie": nota.get("codSnf"),
            "numero_nota_fiscal": nota.get("numNfc"),
            "numero_ordem_compra": nota.get("numOcp") or None,
            "numero_titulo": nota.get("numTit") or None,
            "situacao_nota": nota.get("sitNfc") or "N/A",
            "codigo_forma_pagamento": nota.get("codFpg") or None,
            "data_emissao": self._parse_date(nota.get("datEmi")),
            "data_entrada": self._parse_date(nota.get("datEnt")),
            "data_fechamento_nf": self._parse_date(nota.get("datFec")),
            "data_vencimento_parcela": self._parse_date(
                nota.get("parcela")[0].get("vctPar") if nota.get("parcela") else None
            ),
            "observacao": nota.get("obsNfc") or " ",
            "valor_base": nota.get("vlrBru") or 0,
            "valor_liquido": nota.get("vlrLiq") or 0,
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
        """
        Executa a consulta de notas para a empresa/filial do request.
        """

        # cria DTO
        dto = GetConsultaGeralSeniorDTO(**self.request)

        # usa o Mapper para criar payload
        payload = CreateNotaFiscalEntradaMapper.create(dto)

        # chama o service
        response = self.service.get_nota_fiscal_entrada(payload)

        if not response:
            logger.warning(
                f"Nenhuma nota retornada para empresa {self.request['codigo_empresa']} | filial {self.request['codigo_filial']}"
            )
            return {"status": "ok", "total": 0}

        # serializa a resposta do Zeep
        response = serialize_object(response)
        notas = response.get("notaFiscal", [])

        if not notas:
            logger.warning(f"Nenhuma nota encontrada no response")
            return {"status": "ok", "total": 0}

        # mapeia e filtra notas inválidas
        notas_mapeadas = [n for n in (self._map_nota(n) for n in notas) if n]

        if not notas_mapeadas:
            logger.warning("Nenhuma nota válida para salvar")
            return {"status": "ok", "total": 0}

        # salva no banco
        try:
            await self.repository.bulk_save(notas_mapeadas)
            logger.info(f"{len(notas_mapeadas)} notas salvas com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao salvar notas: {e}", exc_info=True)
            return {"status": "error", "total": 0, "message": str(e)}

        return {"status": "ok", "total": len(notas_mapeadas)}
