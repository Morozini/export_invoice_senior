from zeep import Client, Transport
from zeep.plugins import HistoryPlugin
from requests import Session
import os

class BaseSoapSenior:
    @staticmethod
    def create_client_base(url:str):
        wsdl = f"{os.getenv('URL_BASE_SENIOR')}{url}"
        session = Session()
        transport = Transport(session=session)
        history = HistoryPlugin()
        client = Client(wsdl=wsdl, transport=transport, plugins=[history])
        return client
    