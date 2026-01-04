import json
from app.use_cases.consultar_geral_use_case import ConsultarGeralUseCase
from zeep.helpers import serialize_object


request = {
    "codigo_empresa": "10",
    "codigo_filial": "1001",

}

use_case = ConsultarGeralUseCase(request)
response = use_case.execute()
response = serialize_object(response)

with open("dados.json", "w", encoding="utf-8") as arquivo:
    json.dump(response, arquivo, ensure_ascii=False, indent=4)

print("Dados salvos em dados.json")