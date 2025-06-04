from xml.etree.ElementTree import tostring
import xml.etree.cElementTree as ET

from nfse_soap import authenticate, send_nfse
from nfse_xml import create_lote_rps

SAVE_FILE = True

tomador = {
    "cpf_cnpj": "999999999999",
    "inscricao_municipal": "999999",
    "razao_social": "NOME RAZAO SOCIAL",
    "nome_fantasia": "NOME FANTASIA",
    "endereco": {
        "endereco_tipo": "Rua",
        "logradouro": "LOGRADOURO",
        "numero": "999",
        "complemento": "Casa",
        "bairro": "CENTRO",
        "codigo_municipio": "9999999",
        "municipio": "NOME MUNICIPIO",
        "uf": "ES",
        "cep": "99999999"
    },
    "contato": {
        "telefone": "9999999999",
        "email": "teste@email.com"
    }
}

servicos = [
    {
        "codigo_cnae": "999999999",
        "codigo_servico_116": "99.99",
        "codigo_servico_municipal": "99.99",
        "quantidade": 1,
        "unidade": "UN",
        "descricao": "DESCRICAO SERVIÇO",
        "aliquota": 5.00,
        "valor_servico": 100.00,
        "valor_issqn": 5.00,
        "valor_desconto": 0.00,
        "numero_alvara": 0,
    }
]

valores = {
    "valor_servicos": 100.00,
    "valor_deducoes": 0.00,
    "valor_pis": 0.00,
    "valor_cofins": 0.00,
    "valor_inss": 0.00,
    "valor_ir": 0.00,
    "valor_csll": 0.00,
    "valor_iss": 5.00,
    "valor_outras_retencoes": 0.00,
    "valor_liquido_nfse": 100.02,
    "valor_iss_retido": 0.00
}

observacao = "Observação de teste"

if __name__ == "__main__":
    lote = create_lote_rps(
        id="1",
        numero_lote="1",
        quantidade_rps = 1,
        tomador=tomador,
        servicos=servicos,
        valores=valores,
        observacao=observacao,
    )

    if lote is None:
        raise Exception("Failed to create XML")

    if SAVE_FILE:
        xml_tree = ET.ElementTree(lote)
        with open("xmls/lote_rps.xml", "wb") as file:
            xml_tree.write(file, encoding="utf-8", xml_declaration=True)

    auth_token = authenticate()

    if not auth_token:
        raise Exception("Authentication failed")

    xml_text = tostring(lote, encoding='utf-8', xml_declaration=True)

    response = send_nfse(auth_token, xml_text)
    print(response)
