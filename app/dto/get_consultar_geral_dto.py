
from pydantic import BaseModel

class GetConsultaGeralSeniorDTO(BaseModel):
    codigo_empresa: int
    codigo_filial: int

