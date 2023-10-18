from no import No

class ExpressaoRegular():
    def __init__(self, input) -> None:
        self.nos = self.__ler_input(input)

        for no in self.nos:
            print(no.simbolo, no.numero)

    def __ler_input(self, input):
        input += '#'
        lista_nos = []
        contador_nos = 1
        operadores = ['|', '*']
        parenteses = ['(', ')']

        for index, caracter in enumerate(input):
            if caracter not in parenteses and caracter not in operadores:
                novo_no = No(caracter)
                novo_no.numero = contador_nos
                contador_nos += 1
                lista_nos.append(novo_no)

                if index < len(input) - 1:
                    next_char = input[index + 1]
                    if next_char not in operadores and next_char != parenteses[1]:
                        lista_nos.append(No('.'))
                    elif next_char == parenteses[0]:
                        lista_nos.append(No('.'))

            elif caracter in operadores:
                lista_nos.append(No(caracter))

                if caracter == '*' and index < len(input) - 1:
                    next_char = input[index + 1]
                    if next_char not in operadores and next_char != parenteses[1]:
                        lista_nos.append(No('.'))
                    elif next_char == parenteses[0]:
                        lista_nos.append(No('.'))

            elif caracter == parenteses[1] and index < len(input) - 1:
                next_char = input[index + 1]
                if next_char not in operadores and next_char != parenteses[1]:
                    lista_nos.append(No('.'))

        return lista_nos
