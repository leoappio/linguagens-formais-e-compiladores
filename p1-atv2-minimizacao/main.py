from automatoFinito import AutomatoFinito

entrada = input()
automato = AutomatoFinito(entrada)

automato.minimizar()

automato.imprimir_resultado()
