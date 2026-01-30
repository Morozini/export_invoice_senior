class CreateNotaFiscalEntradaMapper:

    @staticmethod
    def create(
        dto,
        dat_ini: str,
        dat_fim: str,
        indice_pagina: int,
        limite_pagina: int = 100,
    ):
        return {
            "codEmp": str(dto.codigo_empresa),
            "codFil": str(dto.codigo_filial),
            "codSnf": "NFS",
            "datEmiIni": dat_ini,
            "datEmiFim": dat_fim,
            "identificadorSistema": "TL",
            "limitePagina": limite_pagina,
            "indicePagina": indice_pagina,
        }
