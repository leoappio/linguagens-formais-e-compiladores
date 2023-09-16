from transicao import Transicao


class Estado():
    def __init__(self, nome):
        self.nome = nome
        self.transicoes = []

    def add_transicao(self, transicao_nova : Transicao):
        transicao_nao_existe = True
        for transicao in self.transicoes:
            if transicao.simbolo_alfabeto == transicao_nova.simbolo_alfabeto and transicao.estado_destino.nome == transicao_nova.estado_destino.nome:
                transicao_nao_existe = False

        if transicao_nao_existe:
            self.transicoes.append(transicao_nova)
        