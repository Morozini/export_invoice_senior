from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO


class CreateNotaFiscalEntradaMapper:

    @staticmethod
    def create(dto):
        return {
            "codEmp": str(dto.codigo_empresa),
            "codFil": str(dto.codigo_filial),
            "codSnf": "NFS",
            "datEmiIni": "01/01/2026",
            "datEmiFim": "30/12/2026",
            "identificadorSistema": "TL",
            "limitePagina": 5000
        }
    