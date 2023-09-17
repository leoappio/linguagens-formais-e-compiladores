from classeEquivalencia import ClasseEquivalencia
from transicao import Transicao
from estado import Estado


class AutomatoFinito():
    def __init__(self, input):
        estado_inicial, estados_finais, estados, alfabeto = self.__ler_input(input)
        self.estados = estados
        self.estados_finais = estados_finais
        self.estado_inicial = estado_inicial
        self.alfabeto = alfabeto

    
    def minimizar(self):
        self.remover_estados_inalcancaveis()
        self.remover_estados_mortos()
        self.remover_estados_equivalentes()
        

    def remover_estados_inalcancaveis(self):
        estados_alcancaveis = []
        estados_para_processar = [self.estado_inicial]
        while estados_para_processar:
            estado_processando = estados_para_processar.pop()
            estados_alcancaveis.append(estado_processando)
            for transicao in estado_processando.transicoes:
                    if transicao.estado_destino not in estados_para_processar and transicao.estado_destino not in estados_alcancaveis:
                        estados_para_processar.append(transicao.estado_destino)
        
        self.estados = estados_alcancaveis


    def remover_estados_mortos(self):
        nomes_finais = [estado.nome for estado in self.estados_finais]
        estados_vivos = []
        for estado in self.estados:
            if estado.atinge_final_em_algum_caminho(nomes_finais):
                estados_vivos.append(estado)
        
        self.estados = estados_vivos
        self.remover_transicoes_pros_estados_mortos()

    
    def remover_transicoes_pros_estados_mortos(self):
        for estado in self.estados:
            novas_transicoes = []
            for transicao in estado.transicoes:
                if transicao.estado_destino in self.estados:
                    novas_transicoes.append(transicao)
            
            estado.transicoes = novas_transicoes


    def remover_estados_equivalentes(self):
        classe_final = ClasseEquivalencia()
        for estado in self.estados_finais:
            classe_final.adicionar_estado(estado)
            estado.classe_equivalencia = classe_final
            
        classe_nao_final = ClasseEquivalencia()
        for estado in self.estados:
            if not classe_final.contem_estado(estado):
                classe_nao_final.adicionar_estado(estado)
                estado.classe_equivalencia = classe_nao_final

        classes = [classe_nao_final, classe_final]

        minimizado = False
        while not minimizado:
            tamanho_classes = len(classes)
            for simbolo in self.alfabeto:
                novas_classes = []
                for classe in classes:
                    for estado in classe.estados:
                        classe_equivalencia = self.encontrar_classe_equivalencia(novas_classes, classes, estado, simbolo)    
                        if classe_equivalencia is None:
                            classe_equivalencia = ClasseEquivalencia()
                            novas_classes.append(classe_equivalencia)
                        
                        classe_equivalencia.adicionar_estado(estado)
                
                for classe_nova in novas_classes:
                    classe_nova.atualizar_referencias_nos_estados()
                
                classes = novas_classes

            if tamanho_classes == len(novas_classes):
                minimizado = True
                break          
        
        novos_estados = []
        for classe in classes:
            estado_representante = classe.obter_representante()
            novo_estado = Estado(estado_representante.nome)
            novo_estado.classe_equivalencia = classe
            novos_estados.append(novo_estado)
        
        self.estados = novos_estados

        for classe in classes:
            estado_representante = classe.obter_representante()
            estado_representante = next((e for e in self.estados if e.nome == estado_representante.nome), None)
            for simbolo in self.alfabeto:
                for estado in classe.estados:
                    transicoes = estado.get_transicoes_por_simbolo(simbolo)
                    for transicao in transicoes:
                        nome_novo_estado_resultante = transicao.estado_destino.classe_equivalencia.obter_representante().nome
                        estado_destino = next((e for e in self.estados if e.nome == nome_novo_estado_resultante), None)
                        estado_representante.add_transicao(Transicao(estado_representante, simbolo, estado_destino))

        self.atualizar_finais()


    def encontrar_classe_equivalencia(self, classes_novas, classes_antigas, estado, simbolo):
        for classe_nova in classes_novas:
            estado_representante = classe_nova.obter_representante()
            transicao_representante = estado_representante.get_transicoes_por_simbolo(simbolo)
            transicao_estado = estado.get_transicoes_por_simbolo(simbolo)

            if len(transicao_representante) == 0 and len(transicao_estado) == 0:
                if estado.classe_equivalencia == estado_representante.classe_equivalencia:
                    return classe_nova
            
            if len(transicao_representante) != 0 and len(transicao_estado) != 0:
                for classe_antiga in classes_antigas:
                    if transicao_representante[0].estado_destino in classe_antiga.estados and transicao_estado[0].estado_destino in classe_antiga.estados:
                        if estado.classe_equivalencia == estado_representante.classe_equivalencia:
                            return classe_nova
        
        return None 
    

    def unir_transicoes(self):
        for estado in self.estados:
            for simbolo in self.alfabeto:
                if simbolo != '&':
                    nome_novo_estado = ""
                    outras_transicoes = []
                    for transicao in estado.transicoes:
                        if transicao.simbolo_alfabeto == simbolo:
                            nome_novo_estado += transicao.estado_destino.nome
                        else:
                            outras_transicoes.append(transicao)

                    if nome_novo_estado != '':
                        nome_novo_estado = ''.join(sorted(set(nome_novo_estado)))
                        estado_destino_obj = next((e for e in self.estados if e.nome == nome_novo_estado), None)
                        outras_transicoes.append(Transicao(estado, simbolo, estado_destino_obj))
                    
                        estado.transicoes = outras_transicoes


    def atualizar_finais(self):
        novos_finais = []
        for estado_final in self.estados_finais:
            for estado in self.estados:
                if estado_final.nome in estado.nome:
                    novos_finais.append(estado)
        
        self.estados_finais = novos_finais
    
    def __ler_input(self, input):
        parametros = input.split(';')

        estado_inicial_nome = parametros[1]

        estados = []
        estados_ja_visitados = []
        estados_finais_nomes = parametros[2].replace("{","").replace("}","").split(',')

        for transicao_index in range(4, len(parametros)):
            transicao = parametros[transicao_index].split(',')

            if(transicao[0] not in estados_ja_visitados):
                estados_ja_visitados.append(transicao[0])
                estado_origem = Estado(transicao[0])
                estados.append(estado_origem)

                if(transicao[2] not in estados_ja_visitados):
                    estados_ja_visitados.append(transicao[2])
                    estado_destino = Estado(transicao[2])
                    estados.append(estado_destino)

                    estado_origem.add_transicao(Transicao(estado_origem, transicao[1], estado_destino))
                else:
                    estado_destino = next((estado for estado in estados if estado.nome == transicao[2]), None)
                    estado_origem.add_transicao(Transicao(estado_origem, transicao[1], estado_destino))
            else:
                estado_origem = next((estado for estado in estados if estado.nome == transicao[0]), None)

                if(transicao[2] not in estados_ja_visitados):
                    estados_ja_visitados.append(transicao[2])
                    estado_destino = Estado(transicao[2])
                    estados.append(estado_destino)

                    estado_origem.add_transicao(Transicao(estado_origem, transicao[1], estado_destino))
                else:
                    estado_destino = next((estado for estado in estados if estado.nome == transicao[2]), None)
                    estado_origem.add_transicao(Transicao(estado_origem, transicao[1], estado_destino))


        estados_finais = [estado for estado in estados if estado.nome in estados_finais_nomes]

        alfabeto = parametros[3].replace("{","").replace("}","").split(',')

        estado_inicial = next((estado for estado in estados if estado.nome == estado_inicial_nome), None)

        return estado_inicial, estados_finais, estados, alfabeto        


    def imprimir_resultado(self):
        resultado = str(len(self.estados)) + ";"
        
        resultado += self.estado_inicial.nome + ";"
        
        estados_finais_formatados = ["" + estado.nome + "" for estado in sorted(self.estados_finais, key=lambda x: (-len(x.nome), x.nome))]
        resultado += "{" + ",".join(estados_finais_formatados) + "};"
        
        resultado += "{" + ",".join(sorted(self.alfabeto)) + "};"
        
        transicoes_formatadas = []
        for estado in sorted(self.estados, key=lambda x: x.nome):
            for transicao in sorted(estado.transicoes, key=lambda x: (x.estado_origem.nome, x.simbolo_alfabeto)):
                transicoes_formatadas.append(transicao.estado_origem.nome + "," + 
                                            transicao.simbolo_alfabeto + "," + 
                                            transicao.estado_destino.nome)
        resultado += ";".join(transicoes_formatadas)
        
        print(resultado)

        return resultado
