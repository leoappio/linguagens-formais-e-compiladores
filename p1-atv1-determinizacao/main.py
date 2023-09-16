from automatoFinito import AutomatoFinito

entrada = input()
automato = AutomatoFinito(entrada)

#automato.determinizar()

automato.minimizar()

automato.imprimir_resultado()
