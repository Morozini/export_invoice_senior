from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO


class CreateNotaFiscalEntradaMapper:

    @staticmethod
    def create(dto, indice_pagina: int = 1):
        return {
            "codEmp": str(dto.codigo_empresa),
            "codFil": str(dto.codigo_filial),
            "codSnf": "NFS",
            "datEmiIni": "01/01/2026",
            "datEmiFim": "31/12/2026",
            "identificadorSistema": "TL",
            "limitePagina": 50,
            "indicePagina": indice_pagina
        }
    