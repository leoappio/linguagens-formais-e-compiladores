from transicao import Transicao


class Estado():
    def __init__(self, nome):
        self.nome = nome
        self.transicoes = []
        self.classe_equivalencia = None


    def add_transicao(self, transicao_nova : Transicao):
        transicao_nao_existe = True
        for transicao in self.transicoes:
            if transicao.simbolo_alfabeto == transicao_nova.simbolo_alfabeto and transicao.estado_destino.nome == transicao_nova.estado_destino.nome:
                transicao_nao_existe = False

        if transicao_nao_existe:
            self.transicoes.append(transicao_nova)

    
    def get_transicoes_por_simbolo(self, simbolo):
        transicoes = []
        for transicao in self.transicoes:
            if transicao.simbolo_alfabeto == simbolo:
                transicoes.append(transicao)

        return transicoes

    
    def calcular_sigma_fecho(self):
        estados_para_calcular = [self]
        estados_ja_calculados = ''
        nome_sigma_fecho = self.nome

        while estados_para_calcular:
            estado_calculando = estados_para_calcular.pop()
            estados_ja_calculados += estado_calculando.nome
            for transicao in estado_calculando.get_transicoes_por_simbolo('&'):
                if transicao.estado_destino.nome not in estados_ja_calculados:
                    nome_sigma_fecho += transicao.estado_destino.nome
                    estados_para_calcular.append(transicao.estado_destino)

        nome_sigma_fecho = ''.join(sorted(set(nome_sigma_fecho)))
        self.sigma_fecho = nome_sigma_fecho


    def atinge_final_em_algum_caminho(self, nomes_finais):
        estados_para_calcular = [self]
        estados_ja_calculados = ''

        while estados_para_calcular:
            estado_calculando = estados_para_calcular.pop()
            estados_ja_calculados += estado_calculando.nome
            if estado_calculando.nome in nomes_finais:
                return True
            for transicao in estado_calculando.transicoes:
                if transicao.estado_destino.nome not in estados_ja_calculados:
                    estados_para_calcular.append(transicao.estado_destino)
        
        return False
