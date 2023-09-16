from automatoFinito import AutomatoFinito

entrada = input()
automato = AutomatoFinito(entrada)

automato.determinizar()

automato.imprimir_resultado()
