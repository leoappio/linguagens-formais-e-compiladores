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
        self.remover_estados_equivalentes()
        self.remover_estados_mortos()
        

    def remover_estados_inalcancaveis(self):
        estados_processados = []
        estados_para_processar = [self.estado_inicial]

        while estados_para_processar:
            estado_processando = estados_para_processar.pop()
            estados_processados.append(estado_processando)
            for transicao in estado_processando.transicoes:
                    if transicao.estado_destino not in estados_para_processar and transicao.estado_destino not in estados_processados:
                        estados_para_processar.append(transicao.estado_destino)
        
        self.estados = estados_processados


    def remover_estados_mortos(self):
        estados_vivos = set(self.estados_finais)
        novos_estados_vivos = set(self.estados_finais)

        while novos_estados_vivos:
            estados_vivos_atual = novos_estados_vivos
            novos_estados_vivos = set()

            for estado in self.estados:
                for transicao in estado.transicoes:
                    if transicao.estado_destino in estados_vivos_atual:
                        novos_estados_vivos.add(estado)
            
            novos_estados_vivos -= estados_vivos
            estados_vivos.update(novos_estados_vivos)

        self.estados = [estado for estado in self.estados if estado in estados_vivos]

    

    def remover_estados_equivalentes(self):
        ...


    def determinizar(self):
        if self.tem_transicao_epsilon():
            self.__determinizar_com_fecho()
        else:
            self.__determinizar_sem_fecho()


    def __determinizar_com_fecho(self):
        for estado in self.estados:
            estado.calcular_sigma_fecho()    

        novos_estados = []
        estados_a_calcular = [self.estado_inicial.sigma_fecho]

        while estados_a_calcular:
            estado_atual = estados_a_calcular.pop()
            if not self.__existe_estado_com_o_mesmo_nome(novos_estados, estado_atual):
                novo_estado = Estado(estado_atual)
                for simbolo in self.alfabeto:
                    if simbolo != '&':
                        estado_destino_nome = ''
                        for estado in estado_atual:
                            estado_obj = next((e for e in self.estados if e.nome == estado), None)
                            transicoes = estado_obj.get_transicoes_por_simbolo(simbolo)
                            for transicao in transicoes:
                                fecho = transicao.estado_destino.sigma_fecho
                                for estado_fecho in fecho:
                                    estado_fecho_obj = next((e for e in self.estados if e.nome == estado_fecho), None)
                                    novo_estado.add_transicao(Transicao(novo_estado, simbolo, estado_fecho_obj))
                                    estado_destino_nome += estado_fecho_obj.nome
                        
                            estado_destino_nome = ''.join(sorted(set(estado_destino_nome)))
                            
                            estados_a_calcular.append(estado_destino_nome)

                if novo_estado.nome != '':
                    novos_estados.append(novo_estado)
            
        self.estados = novos_estados

        self.unir_transicoes()
        self.atualizar_finais()
        self.atualizar_estado_inicial()
        self.atualizar_alfabeto()


    def __determinizar_sem_fecho(self):
        novos_estados = [self.estado_inicial]
        estados_a_calcular = [self.estado_inicial]

        while estados_a_calcular:
            estado_atual = estados_a_calcular.pop()

            for simbolo in self.alfabeto:
                nome_novo_estado = ""
                for transicao in estado_atual.transicoes:
                    if transicao.simbolo_alfabeto == simbolo:
                        nome_novo_estado += transicao.estado_destino.nome

                nome_novo_estado = ''.join(sorted(set(nome_novo_estado)))

                if not self.__existe_estado_com_o_mesmo_nome(novos_estados, nome_novo_estado):
                    novo_estado_obj = Estado(nome_novo_estado)

                    for estado in nome_novo_estado:
                        estado_obj = next((e for e in self.estados if e.nome == estado), None)
                        for transicao in estado_obj.transicoes:
                            novo_estado_obj.add_transicao(transicao)

                    novos_estados.append(novo_estado_obj)
                    estados_a_calcular.append(novo_estado_obj)

        self.estados = novos_estados

        self.unir_transicoes()
        self.atualizar_finais()


    def __existe_estado_com_o_mesmo_nome(self,novos_estados, nome):
        for estado in novos_estados:
            if estado.nome == nome:
                return True
            
        return False
    

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
    

    def atualizar_estado_inicial(self):
        nome_sigma_fecho = self.estado_inicial.sigma_fecho
        estado_sigma_fecho_obj = next((e for e in self.estados if e.nome == nome_sigma_fecho), None)
        self.estado_inicial = estado_sigma_fecho_obj


    def atualizar_alfabeto(self):
        self.alfabeto.remove('&')


    def tem_transicao_epsilon(self):
        for estado in self.estados:
            for transicao in estado.transicoes:
                if transicao.simbolo_alfabeto == "&":
                    return True
        return False
    
    
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
        
        resultado += "{" + self.estado_inicial.nome + "};"
        
        estados_finais_formatados = ["{" + estado.nome + "}" for estado in sorted(self.estados_finais, key=lambda x: (-len(x.nome), x.nome))]
        resultado += "{" + ",".join(estados_finais_formatados) + "};"
        
        resultado += "{" + ",".join(sorted(self.alfabeto)) + "};"
        
        transicoes_formatadas = []
        for estado in sorted(self.estados, key=lambda x: x.nome):
            for transicao in sorted(estado.transicoes, key=lambda x: (x.estado_origem.nome, x.simbolo_alfabeto)):
                transicoes_formatadas.append("{" + transicao.estado_origem.nome + "}," + 
                                            transicao.simbolo_alfabeto + "," + 
                                            "{" + transicao.estado_destino.nome + "}")
        resultado += ";".join(transicoes_formatadas)
        
        print(resultado)

        return resultado
