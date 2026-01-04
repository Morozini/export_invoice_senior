
from pydantic import BaseModel

class GetConsultaGeralSeniorDTO(BaseModel):
    codigo_empresa: str
    codigo_filial: str

