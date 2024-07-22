# Importar bibliotecas necessárias
import csv  # Biblioteca para manipulação de ficheiros CSV
import random  # Biblioteca para geração de números aleatórios


# Função para gerar um cartão de bingo
def gerar():
    lista = []  # Lista para armazenar as linhas do cartão
    numeros = random.sample(range(1, 99), 15)  # Gerar 15 números aleatórios únicos entre 1 e 98

    # Dividir os 15 números em 3 linhas de 5 números cada
    for i in range(3):
        lista.append(numeros[i * 5:(i + 1) * 5])

    return lista  # Retornar o cartão gerado


# Classe para representar um cartão de bingo
class CARTAO:
    def __init__(self, nome):
        # Inicializar o nome do jogador
        self.nome = nome
        # Gerar um cartão de bingo para o jogador
        self.cartao = gerar()
        # Inicializar o número de iterações para linha completa
        self.itera_linha = 0
        # Imprimir o cartão
        print(self.cartao)
        # Inicializar uma matriz 3x5 para marcar o cartão
        self.marcaCartao = [[False, False, False, False, False],
                            [False, False, False, False, False],
                            [False, False, False, False, False]]

    # Método para marcar um número no cartão
    def marcacao(self, numero):
        # Percorrer todas as posições do cartão
        for linhas in range(3):
            for colunas in range(5):
                # Verificar se o número sorteado está no cartão
                if self.cartao[linhas][colunas] == numero:
                    # Marcar a posição correspondente
                    self.marcaCartao[linhas][colunas] = True
                    # Imprimir a mensagem de cartão marcado
                    print(f"Cartão marcado! Linha: {linhas + 1}, Coluna: {colunas + 1} {self.nome}\n")

    # Método para verificar se alguma linha está completa
    def verificar_linha(self):
        # Verificar cada linha do cartão
        for i in range(3):
            # Se todos os elementos da linha estão marcados, a linha está completa
            if all(self.marcaCartao[i]):
                return i  # Retornar o índice da linha completa
        return None  # Retornar None se nenhuma linha está completa

    # Método para verificar se o jogador fez bingo (todas as linhas completas)
    def isbingo(self):
        lista_linas = [False, False, False]
        for i in range(3):
            if all(self.marcaCartao[i]):
                lista_linas[i] = True

        # Retornar True se todas as linhas estão completas (bingo)
        return all(lista_linas)


# Classe para representar o jogo
class JOGAR:
    def __init__(self, jogador1, jogador2):
        # Inicializar os jogadores
        self.jogador1 = jogador1
        self.jogador2 = jogador2
        # Inicializar a lista de números sorteados
        self.lista_numeros = []
        # Inicializar o número de iterações
        self.iteratoes = 0
        # Inicializar as variáveis para linha completa e bingo
        self.linha_completa_nome = None
        self.linha_completa = None
        self.linha_completa_iteracao = None
        self.bingo = None

    # Método para iniciar o jogo
    def inicio(self):
        # Continuar o jogo até que um dos jogadores faça bingo
        while not self.jogador1.isbingo() and not self.jogador2.isbingo():
            # Incrementar o número de iterações
            self.iteratoes += 1
            # Imprimir a mensagem de iteração
            print(f"#############################################################################")
            print(f"\nIteração {self.iteratoes}\n")
            # Sortear um número
            numero = self.sorteio()
            # Marcar o número no cartão do jogador 1
            self.jogador1.marcacao(numero)
            # Marcar o número no cartão do jogador 2
            self.jogador2.marcacao(numero)
            # Imprimir os cartões dos jogadores
            print(self.jogador1.marcaCartao)
            print(self.jogador2.marcaCartao)

            # Verificar se algum jogador completou uma linha pela primeira vez
            if self.linha_completa is None:
                if self.jogador1.verificar_linha() is not None:
                    self.linha_completa_nome = self.jogador1.nome
                    self.linha_completa_iteracao = self.iteratoes
                    self.linha_completa = self.jogador1.verificar_linha()

            if self.linha_completa is None:
                if self.jogador2.verificar_linha() is not None:
                    self.linha_completa_nome = self.jogador2.nome
                    self.linha_completa_iteracao = self.iteratoes
                    self.linha_completa = self.jogador2.verificar_linha()

        # Verificar qual jogador fez bingo
        if self.jogador1.isbingo():
            self.bingo = jogador1.nome
        else:
            self.bingo = jogador2.nome

        print(f"\nBINGO!!! {self.bingo}")
        print(f"\n{self.linha_completa_nome} fez linha na iteração {self.linha_completa_iteracao}\n")
        print(f"#############################################################################")

    # Método para sortear um número
    def sorteio(self):
        numero = random.randint(1, 99)
        # Verificar se o número já foi sorteado
        if numero not in self.lista_numeros:
            print(f"Número sorteado {numero}.")
            self.lista_numeros.append(numero)
            return numero
        print(f"O número já saiu {numero}.\n")
        print(f"Lista de números já sorteados \n{self.lista_numeros}\n")
        return 0

    # Método para salvar os resultados do jogo num ficheiro CSV
    def save_csv(self):
        with open('results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            header_row = ["jogador", "coluna1", "coluna2", "coluna3", "coluna4", "coluna5", "linha", "bingo"]
            writer.writerow(header_row)

            # Salvar os dados do jogador 1
            for i in range(3):
                row = [self.jogador1.nome]
                row.extend(self.jogador1.cartao[i])
                if i == self.linha_completa and self.linha_completa_nome == self.jogador1.nome:
                    row.append(self.linha_completa_iteracao)
                else:
                    row.append('x')
                if i == 0 and self.bingo == self.jogador1.nome:
                    row.append(self.iteratoes)
                else:
                    row.append('x')
                writer.writerow(row)

            # Salvar os dados do jogador 2
            for i in range(3):
                row = [self.jogador2.nome]
                row.extend(self.jogador2.cartao[i])
                if i == self.linha_completa and self.linha_completa_nome == self.jogador2.nome:
                    row.append(self.linha_completa_iteracao)
                else:
                    row.append('x')
                if i == 0 and self.bingo == self.jogador2.nome:
                    row.append(self.iteratoes)
                else:
                    row.append('x')
                writer.writerow(row)


# Criar instâncias de CARTAO para dois jogadores e iniciar o jogo
jogador1 = CARTAO("Nuno")
jogador2 = CARTAO("Joao")
jogar = JOGAR(jogador1, jogador2)
jogar.inicio()
jogar.save_csv()
