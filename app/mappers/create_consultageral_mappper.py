from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO


class CreateNotaFiscalEntradaMapper:

    @staticmethod
    def create(dto):
        return {
            "codEmp": str(dto.codigo_empresa),
            "codFil": str(dto.codigo_filial),
            "codSnf": "NFS",
            "datEmiIni": "10/12/2025",
            "datEmiFim": "30/12/2025",
            "identificadorSistema": "TL",
        }