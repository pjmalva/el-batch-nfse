from zeep import Client
from zeep.transports import Transport

WSDL_URL = "https://es-colatina-pm-nfs.cloud.el.com.br/RpsServiceService?wsdl"
WSDL_USER = "22627105000108"
WSDL_PASSWORD = "20102016"

def authenticate() -> str | None:
    soap_client = Client(WSDL_URL)
    return soap_client.service.autenticarContribuinte(
        identificacaoPrestador=WSDL_USER,
        senha=WSDL_PASSWORD
    )

def send_nfse(token: str, xml: str) -> str | None:
    soap_client = Client(WSDL_URL)
    response = soap_client.service.EnviarLoteRpsEnvio(
        identificacaoPrestador=WSDL_USER,
        hashIdentificador=token,
        arquivo=xml,
    )
    return response if response else None
