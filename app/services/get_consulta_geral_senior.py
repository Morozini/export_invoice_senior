import logging
from dotenv import load_dotenv
import os
from zeep.exceptions import TransportError
from requests.exceptions import ConnectTimeout
from urllib3.exceptions import MaxRetryError
from app.helpers.base_zeep import BaseSoapSenior

load_dotenv()

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class GetConsultaGeralService:
    def __init__(self):
        self.base_soap_senior = BaseSoapSenior

    def get_nota_fiscal_entrada(self, dto) -> dict:
        wsdl_url = "g5-senior-services/sapiens_Synccom_senior_g5_co_mcm_cpr_notafiscalentrada?wsdl"
        client = self.base_soap_senior.create_client_base(wsdl_url)
        usuario = os.getenv('USER_SENIOR')
        senha = os.getenv('PASSWORD_SENIOR')
        try:
            return client.service.ConsultarGeral_5(
                user=usuario,
                password=senha,
                encryption=0,
                parameters=dto
            )
        except (ConnectTimeout, MaxRetryError, TransportError) as specific_error:
            logging.error(f"Erro específico na conexão com o webservice: {specific_error}")
            return {
                'retorno': 'Erro ao conectar com o webservice. Por favor, tente novamente mais tarde.',
                'situacao': 'erro',
                'message': str(specific_error)
            }
        except Exception as e:
            logging.error(f"Erro inesperado: {e}", exc_info=True)
            return {
                'retorno': 'Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.',
                'situacao': 'erro',
                'message': str(e)
            }