class ClasseEquivalencia():
    def __init__(self):
        self.estados = []

    def adicionar_estado(self, estado):
        self.estados.append(estado)

    def remover_estado(self, estado):
        if estado in self.estados:
            self.estados.remove(estado)

    def contem_estado(self, estado):
        return estado in self.estados

    def obter_representante(self):
        if not self.estados:
            return None
        estados_ordenados = sorted(self.estados, key=lambda estado: estado.nome)
        return estados_ordenados[0]
    
    def atualizar_referencias_nos_estados(self):
        for estado in self.estados:
            estado.classe_equivalencia = self