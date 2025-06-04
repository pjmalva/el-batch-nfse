import xml.etree.cElementTree as ET
from datetime import datetime

DADOS_PRESTADOR = {
    "cpf_cnpj": "99999999000199",
    "inscricao_municipal": "9999999",
    "razao_social": "NOME RAZAO SOCIAL",
    "nome_fantasia": "NOME FANTASIA",
    "incentivador_cultural": 2,
    "optante_simples_nacional": 2,
    "natureza_operacao": 1,
    "regime_especial_tributacao": 1,
    "endereco": {
        "logradouro_tipo": "Rua",
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
        "email": "teste@teste.com"
    }
}

def create_root(name: str, attributes: dict | None = None) -> ET.Element:
     return ET.Element(name, **attributes if attributes else {})

def add_child(
    parent: ET.Element, 
    child_name: str, 
    child_text: str | None = None
):
    child = ET.SubElement(parent, child_name)
    if child_text is not None:
        child.text = child_text
    return parent

def create_lote_rps(
    id: str,
    numero_lote: str,
    quantidade_rps: int,
    tomador: dict,
    servicos: list,
    valores: dict,
    observacao: str | None = None,
) -> ET.Element:
    root = create_root(
        'LoteRps',
        {
            "xmlns": "http://www.el.com.br/nfse/xsd/el-nfse.xsd",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "xsi:schemaLocation": "http://www.el.com.br/nfse/xsd/el-nfse.xsd el-nfse.xsd "
        }   
    )
    
    root = add_child(root, "Id", id)
    root = add_child(root, "NumeroLote", numero_lote)
    root = add_child(root, "QuantidadeRps", str(quantidade_rps))

    identificacao_prestador = ET.SubElement(root, "IdentificacaoPrestador")
    add_child(identificacao_prestador, "CpfCnpj", DADOS_PRESTADOR["cpf_cnpj"])
    add_child(identificacao_prestador, "IndicacaoCpfCnpj", str(2))
    add_child(identificacao_prestador, "InscricaoMunicipal", DADOS_PRESTADOR["inscricao_municipal"])

    lista_rps = ET.SubElement(root, "ListaRps")

    create_rps(
        parent=lista_rps,
        id="0000001",
        local_prestacao=1,
        iss_retido=0,
        tomador=tomador,
        servicos=servicos,
        valores=valores,
        observacao=observacao
    )

    return root

def create_rps(
    parent: ET.Element,
    id: str,
    local_prestacao: int,
    iss_retido: int,
    tomador: dict,
    servicos: list,
    valores: dict,
    observacao: str | None = None
):
    data_emissao = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    rps = add_child(parent, "Rps")
    add_child(rps, "Id", id)
    add_child(rps, "LocalPrestacao", str(local_prestacao))
    add_child(rps, "IssRetido", str(iss_retido))
    add_child(rps, "DataEmissao", data_emissao)

    identificacao_rps = ET.SubElement(rps, "IdentificacaoRps")
    add_child(identificacao_rps, "Numero", "0000001")
    add_child(identificacao_rps, "Serie", "1")
    add_child(identificacao_rps, "Tipo", "1")

    dados_prestador = ET.SubElement(rps, "DadosPrestador")

    identificacao_prestador = ET.SubElement(dados_prestador, "IdentificacaoPrestador")
    add_child(identificacao_prestador, "CpfCnpj", DADOS_PRESTADOR["cpf_cnpj"])
    add_child(identificacao_prestador, "IndicacaoCpfCnpj", str(2))
    add_child(identificacao_prestador, "InscricaoMunicipal", DADOS_PRESTADOR["inscricao_municipal"])

    add_child(dados_prestador, "RazaoSocial", DADOS_PRESTADOR["razao_social"])
    add_child(dados_prestador, "NomeFantasia", DADOS_PRESTADOR["nome_fantasia"])
    add_child(dados_prestador, "IncentivadorCultural", str(DADOS_PRESTADOR["incentivador_cultural"]))
    add_child(dados_prestador, "OptanteSimplesNacional", str(DADOS_PRESTADOR["optante_simples_nacional"]))
    add_child(dados_prestador, "NaturezaOperacao", str(DADOS_PRESTADOR["natureza_operacao"]))
    add_child(dados_prestador, "RegimeEspecialTributacao", str(DADOS_PRESTADOR["regime_especial_tributacao"]))

    endereco = ET.SubElement(dados_prestador, "Endereco")
    add_child(endereco, "LogradouroTipo", DADOS_PRESTADOR["endereco"]["logradouro_tipo"])
    add_child(endereco, "Logradouro", DADOS_PRESTADOR["endereco"]["logradouro"])
    add_child(endereco, "LogradouroNumero", DADOS_PRESTADOR["endereco"]["numero"])
    add_child(endereco, "LogradouroComplemento", DADOS_PRESTADOR["endereco"]["complemento"])
    add_child(endereco, "Bairro", DADOS_PRESTADOR["endereco"]["bairro"])
    add_child(endereco, "CodigoMunicipio", DADOS_PRESTADOR["endereco"]["codigo_municipio"])
    add_child(endereco, "Municipio", DADOS_PRESTADOR["endereco"]["municipio"])
    add_child(endereco, "Uf", DADOS_PRESTADOR["endereco"]["uf"])
    add_child(endereco, "Cep", DADOS_PRESTADOR["endereco"]["cep"])

    contato = ET.SubElement(dados_prestador, "Contato")
    add_child(contato, "Telefone", DADOS_PRESTADOR["contato"]["telefone"])
    add_child(contato, "Email", DADOS_PRESTADOR["contato"]["email"])

    dados_tomador = ET.SubElement(rps, "DadosTomador")

    identificacao_tomador = ET.SubElement(dados_tomador, "IdentificacaoTomador")
    add_child(identificacao_tomador, "CpfCnpj", tomador["cpf_cnpj"])
    add_child(identificacao_tomador, "IndicacaoCpfCnpj", "1")
    add_child(identificacao_tomador, "InscricaoMunicipal", tomador["inscricao_municipal"])
    add_child(dados_tomador, "RazaoSocial", tomador["razao_social"])
    add_child(dados_tomador, "NomeFantasia", tomador["nome_fantasia"])

    endereco_tomador = ET.SubElement(dados_tomador, "Endereco")
    add_child(endereco_tomador, "LogradouroTipo", tomador["endereco"]["endereco_tipo"])
    add_child(endereco_tomador, "Logradouro", tomador["endereco"]["logradouro"])
    add_child(endereco_tomador, "LogradouroNumero", tomador["endereco"]["numero"])

    if "complemento" in tomador["endereco"] and tomador["endereco"]["complemento"]:
        add_child(endereco_tomador, "LogradouroComplemento", tomador["endereco"]["complemento"])

    add_child(endereco_tomador, "Bairro", tomador["endereco"]["bairro"])
    add_child(endereco_tomador, "CodigoMunicipio", tomador["endereco"]["codigo_municipio"])
    add_child(endereco_tomador, "Municipio", tomador["endereco"]["municipio"])
    add_child(endereco_tomador, "Uf", tomador["endereco"]["uf"])
    add_child(endereco_tomador, "Cep", tomador["endereco"]["cep"])

    contato_tomador = ET.SubElement(dados_tomador, "Contato")
    add_child(contato_tomador, "Telefone", tomador["contato"]["telefone"])
    add_child(contato_tomador, "Email", tomador["contato"]["email"])

    lista_servicos = ET.SubElement(rps, "ListaServicos")
    for servico in servicos:
        servico_element = ET.SubElement(lista_servicos, "Servico")
        add_child(servico_element, "CodigoCnae", servico["codigo_cnae"])
        add_child(servico_element, "CodigoServico116", servico["codigo_servico_116"])
        add_child(servico_element, "CodigoServicoMunicipal", servico["codigo_servico_municipal"])
        add_child(servico_element, "Quantidade", str(servico["quantidade"]))
        add_child(servico_element, "Unidade", servico["unidade"])
        add_child(servico_element, "Descricao", servico["descricao"])
        add_child(servico_element, "Aliquota", str(servico["aliquota"]))
        add_child(servico_element, "ValorServicos", str(servico["valor_servico"]))
        add_child(servico_element, "ValorIssqn", str(servico["valor_issqn"]))
        add_child(servico_element, "ValorDesconto", str(servico["valor_desconto"]))
        add_child(servico_element, "NumeroAlvara", str(servico["numero_alvara"]))

    valores_element = ET.SubElement(rps, "Valores")
    add_child(valores_element, "ValorServicos", str(valores["valor_servicos"]))
    add_child(valores_element, "ValorDeducoes", str(valores["valor_deducoes"]))
    add_child(valores_element, "ValorPis", str(valores["valor_pis"]))
    add_child(valores_element, "ValorCofins", str(valores["valor_cofins"]))
    add_child(valores_element, "ValorInss", str(valores["valor_inss"]))
    add_child(valores_element, "ValorIr", str(valores["valor_ir"]))
    add_child(valores_element, "ValorCsll", str(valores["valor_csll"]))
    add_child(valores_element, "ValorIss", str(valores["valor_iss"]))
    add_child(valores_element, "ValorOutrasRetencoes", str(valores["valor_outras_retencoes"]))
    add_child(valores_element, "ValorLiquidoNfse", str(valores["valor_liquido_nfse"]))
    add_child(valores_element, "ValorIssRetido", str(valores["valor_iss_retido"]))

    if observacao:
        observacao_rps = ET.SubElement(rps, "Observacao")
        observacao_rps.text = observacao

    # add_child(rps, "Status", "1")  # Status 1: Normal

    return rps
