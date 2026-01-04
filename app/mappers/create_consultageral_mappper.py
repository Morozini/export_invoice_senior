from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO


class CreateConsultaGeralMapper:

    @staticmethod
    def create(dto: GetConsultaGeralSeniorDTO):
        return {
            "codEmp":str(dto.codigo_empresa),
            "codSnf": "NFS",
            "codFil":str(dto.codigo_filial),
            "datEmiIni": "01/12/2025",
            "datEmiFim": "30/12/2025",
            "numNfc": "1254",
            "identificadorSistema": "TL",
        }