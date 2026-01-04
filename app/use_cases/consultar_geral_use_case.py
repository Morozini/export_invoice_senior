
from app.dto.get_consultar_geral_dto import GetConsultaGeralSeniorDTO
from app.mappers.create_consultageral_mappper import CreateConsultaGeralMapper
from app.services.get_consulta_geral_senior import GetConsultaGeralService


class ConsultarGeralUseCase:
    def __init__(self, request):
        self.request = request
        payload = GetConsultaGeralSeniorDTO(**request)
        self.payload_mapper = CreateConsultaGeralMapper.create(payload)
        self.service = GetConsultaGeralService()

    def execute(self):
        return self.service.get_nota_fiscal_entrada(self.payload_mapper)
    
    def validation(self, request):
        print(request)
        list_response = []
        lista_notas = request.notaFiscal

        if not lista_notas:
            return {
                'retorno': 'Nota Fiscal não informada.',
                'situacao': 'erro'
            }
        for notaFiscal in lista_notas:
            codigo_empresa = notaFiscal.codEmp
            codigo_filial = notaFiscal.codFil
            data_emissao = notaFiscal.datEmi
            nuemro_nota_fiscal = notaFiscal.numNfv
            situacao_nota_fiscal = notaFiscal.sitNfv

            
            list_response.append({
                'codigo_empresa': codigo_empresa,
                'codigo_filial': codigo_filial,
                'data_emissao': data_emissao,
                'nuemro_nota_fiscal': nuemro_nota_fiscal,
                'situacao_nota_fiscal': situacao_nota_fiscal,
            })
            return list_response
        
    def validation_rateio(self, request):
        list_response_rateio = []
        lista_titulos = request.notaFiscal

        if not lista_titulos:
            return {
                'retorno': 'Nenhum título informado.',
                'situacao': 'erro'
            }

        for titulo in lista_titulos:
            if not hasattr(titulo, "rateio") or not titulo.rateio:
                return {
                    'retorno': f'Rateio não informado para o título.',
                    'situacao': 'erro'
                }

            for rateio in titulo.rateio:
                list_response_rateio.append({
                    'transacao_saida': rateio.tnsSer,
                    'codigo_cta_financeira': rateio.ctaFin,
                    'codigo_centro_de_custo': rateio.codCcu,
                    'codigo_fase': rateio.codFpj,
                    'codigo_projeto': rateio.numPrj,
                    'valor_rateio': rateio.vlrRat
                })

        return list_response_rateio
    
    def validation_acumulador(self, request):
        list_response_acumulador = []
        lista_notas = request.notaFiscal

        if not lista_notas:
            return {
                'retorno': 'Nenhuma nota fiscal informada.',
                'situacao': 'erro'
            }

        for nota in lista_notas:
            if not hasattr(nota, "camposUsuarioNotaFiscal") or not nota.camposUsuarioNotaFiscal:
                return {
                    'retorno': 'Acumulador não informado na nota fiscal.',
                    'situacao': 'erro'
                }

            for campo in nota.camposUsuarioNotaFiscal:
                if campo.campo == "USU_CODACU":
                    list_response_acumulador.append({
                        'codigo_acumulador': campo.valor
                    })

        return list_response_acumulador
    
    def validation_parcela(self, request):
        list_response_parcela = []
        lista_notas = request.notaFiscal

        if not lista_notas:
            return {
                'retorno': 'Nenhuma nota fiscal informada.',
                'situacao': 'erro'
            }

        for nota in lista_notas:
            if not hasattr(nota, "parcela") or not nota.parcela:
                return {
                    'retorno': f'Parcela não informada para a nota fiscal {getattr(nota, "numNfv", "")}.',
                    'situacao': 'erro'
                }

            for parcela in nota.parcela:
                list_response_parcela.append({
                    'codigo_empresa': parcela.codEmp,
                    'codigo_filial': parcela.codFil,
                    'usuario_gerador': parcela.usuGer,
                    'numero_titulo': parcela.numTit,
                    'valor_parcela': parcela.vlrPar,
                    'vencimento_parcela': parcela.vctPar,
                })

        return list_response_parcela
    
    def validation_servico(self, request):
        list_response_servico = []
        lista_notas = request.notaFiscal

        if not lista_notas:
            return {
                'retorno': 'Nenhuma nota fiscal informada.',
                'situacao': 'erro'
            }

        for nota in lista_notas:
            if not hasattr(nota, "servico") or not nota.servico:
                return {
                    'retorno': f'Serviço não informado para a nota fiscal {getattr(nota, "numNfv", "")}.',
                    'situacao': 'erro'
                }

            for servico in nota.servico:
                list_response_servico.append({
                    'codigo_servico': servico.codSer,
                    'descricao_servico': servico.cplIsv,
                    'valor_servico': servico.preUni,
                    'valor_iss': servico.vlrIss,
                    'valor_pis': servico.vlrPit,
                    'valor_cofins': servico.vlrCrt,
                    'valor_csll': servico.vlrCsl,
                    'valor_ir': servico.vlrIrf,
                })

        return list_response_servico

