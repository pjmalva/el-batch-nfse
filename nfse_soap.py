import os
from zeep import Client


def authenticate() -> str | None:
    url = os.getenv("WSDL_URL")
    user = os.getenv("WSDL_USER")
    passwd = os.getenv("WSDL_PASSWORD")

    if not url:
        raise ValueError("WSDL_URL must be set in environment variables.")

    if not user:
        raise ValueError("WSDL_USER must be set in environment variables.")

    if not passwd:
        raise ValueError("WSDL_PASSWORD must be set in environment variables.")

    soap_client = Client(url)
    return soap_client.service.autenticarContribuinte(
        identificacaoPrestador=user,
        senha=passwd,
    )

def send_nfse(token: str, xml: str) -> str | None:
    url = os.getenv("WSDL_URL")
    user = os.getenv("WSDL_USER")

    if not url:
        raise ValueError("WSDL_URL must be set in environment variables.")

    if not user:
        raise ValueError("WSDL_USER must be set in environment variables.")

    if not token:
        raise ValueError("Token must be provided for sending NFSe.")

    if not xml:
        raise ValueError("XML content must be provided for sending NFSe.")

    soap_client = Client(url)
    response = soap_client.service.EnviarLoteRpsEnvio(
        identificacaoPrestador=user,
        hashIdentificador=token,
        arquivo=xml,
    )
    return response if response else None
