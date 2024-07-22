import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLineEdit, QComboBox, QLabel, QSplitter, QFileDialog, QMessageBox
import pandas as pd
import matplotlib.pyplot as plt

# Define a classe Filme para representar um filme no sistema
class Filme:
    def __init__(self, nome, realizador, ano, classificacao, genero, sala, reservas):
        self.nome = nome
        self.realizador = realizador
        self.ano = ano
        self.classificacao = classificacao
        self.genero = genero
        self.sala = sala
        self.bilhetes_disponiveis = reservas

# Define a classe Cinema para gerenciar uma coleção de filmes
class Cinema:
    def __init__(self):
        self.filmes = []

    def adicionar_filme(self, filme):
        self.filmes.append(filme)

    def remover_filme(self, indice):
        if 0 <= indice < len(self.filmes):
            del self.filmes[indice]

    def remover_reservas(self):
        for filme in self.filmes:
            filme.bilhetes_disponiveis = 10

    def reservar_bilhete(self, filme, quantidade):
        if filme.bilhetes_disponiveis >= quantidade:
            filme.bilhetes_disponiveis -= quantidade
            return True
        else:
            return False

    def carregar_filmes(self, csv_path):
        df = pd.read_csv(csv_path)  # Lê o arquivo CSV usando pandas
        for _, row in df.iterrows():
            filme = Filme(row['Nome'], row['Realizador'], row['Ano'], row['Classificação'], row['Genero'], row['Sala'], row['Reservas'])
            self.adicionar_filme(filme)

    def salvar_filmes(self, csv_path):
        data = [{'Nome': filme.nome, 'Realizador': filme.realizador, 'Ano': filme.ano, 'Classificação': filme.classificacao, 'Genero': filme.genero, 'Sala': filme.sala, 'Reservas': filme.bilhetes_disponiveis} for filme in self.filmes]
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)  # Salva a lista de filmes em um arquivo CSV

# Define a classe MainWindow para criar a interface gráfica do usuário
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cinema = Cinema()  # Cria uma instância da classe Cinema

        self.setWindowTitle("Sistema de Gestão de Cinema")
        self.setGeometry(100, 100, 1200, 600)

        main_layout = QHBoxLayout()

        # Cria e configura a tabela para exibir filmes
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Nome", "Realizador", "Ano", "Classificação", "Género", "Sala", "Reservas"])

        self.splitter = QSplitter()
        self.splitter.addWidget(self.table)

        form_layout = QVBoxLayout()

        # Campos para adicionar um filme
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do Filme")
        self.realizador_input = QLineEdit()
        self.realizador_input.setPlaceholderText("Realizador")
        self.ano_input = QLineEdit()
        self.ano_input.setPlaceholderText("Ano")
        self.classificacao_input = QLineEdit()
        self.classificacao_input.setPlaceholderText("Classificação (0.0 - 10.0)")
        self.genero_input = QComboBox()
        self.genero_input.addItems(["Ação", "Comédia"])
        self.sala_input = QLineEdit()
        self.sala_input.setPlaceholderText("Sala")
        self.reservas_input = QLineEdit()
        self.reservas_input.setPlaceholderText("Reservas")
        self.add_button = QPushButton("Adicionar Filme")
        self.add_button.clicked.connect(self.adicionar_filme)  # Conecta o botão à função de adicionar filme
        self.add_button.setStyleSheet("background-color: lightgreen;")

        form_layout.addWidget(QLabel("Adicionar Filme"))
        form_layout.addWidget(self.nome_input)
        form_layout.addWidget(self.realizador_input)
        form_layout.addWidget(self.ano_input)
        form_layout.addWidget(self.classificacao_input)
        form_layout.addWidget(self.genero_input)
        form_layout.addWidget(self.sala_input)
        form_layout.addWidget(self.reservas_input)
        form_layout.addWidget(self.add_button)

        # Campos para reservar bilhetes
        self.reservar_input = QLineEdit()
        self.reservar_input.setPlaceholderText("Quantidade de Bilhetes")
        self.reserve_button = QPushButton("Reservar Bilhete")
        self.reserve_button.clicked.connect(self.reservar_bilhete)  # Conecta o botão à função de reservar bilhete
        self.reserve_button.setStyleSheet("background-color: lightblue;")

        form_layout.addWidget(QLabel("Reservar Bilhetes"))
        form_layout.addWidget(self.reservar_input)
        form_layout.addWidget(self.reserve_button)

        # Botão para remover um filme
        self.remove_button = QPushButton("Remover Filme")
        self.remove_button.clicked.connect(self.remover_filme)  # Conecta o botão à função de remover filme
        self.remove_button.setStyleSheet("background-color: lightcoral;")

        form_layout.addWidget(self.remove_button)

        # Outros botões
        self.remove_reserves_button = QPushButton("Remover Reservas")
        self.remove_reserves_button.clicked.connect(self.remover_reservas)  # Conecta o botão à função de remover reservas
        self.remove_reserves_button.setStyleSheet("background-color: lightcoral;")

        self.load_csv_button = QPushButton("Carregar CSV")
        self.load_csv_button.clicked.connect(self.carregar_csv)  # Conecta o botão à função de carregar CSV
        self.load_csv_button.setStyleSheet("background-color: lightyellow;")

        self.save_csv_button = QPushButton("Salvar CSV")
        self.save_csv_button.clicked.connect(self.salvar_csv)  # Conecta o botão à função de salvar CSV
        self.save_csv_button.setStyleSheet("background-color: lightpink;")

        self.show_graph_button = QPushButton("Mostrar Gráfico")
        self.show_graph_button.clicked.connect(self.mostrar_grafico)  # Conecta o botão à função de mostrar gráfico
        self.show_graph_button.setStyleSheet("background-color: lightgray;")

        form_layout.addWidget(self.remove_reserves_button)
        form_layout.addWidget(self.load_csv_button)
        form_layout.addWidget(self.save_csv_button)
        form_layout.addWidget(self.show_graph_button)

        form_layout.addStretch()
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        self.splitter.addWidget(form_widget)

        main_layout.addWidget(self.splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # Atualiza a tabela com a lista de filmes do cinema
    def atualizar_tabela(self):
        self.table.setRowCount(0)
        for filme in self.cinema.filmes:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(filme.nome))
            self.table.setItem(row_position, 1, QTableWidgetItem(filme.realizador))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(filme.ano)))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(filme.classificacao)))
            self.table.setItem(row_position, 4, QTableWidgetItem(filme.genero))
            self.table.setItem(row_position, 5, QTableWidgetItem(str(filme.sala)))
            self.table.setItem(row_position, 6, QTableWidgetItem(str(filme.bilhetes_disponiveis)))

    # Adiciona um novo filme à lista
    def adicionar_filme(self):
        nome = self.nome_input.text()
        realizador = self.realizador_input.text()
        ano = self.ano_input.text()
        classificacao = self.classificacao_input.text()
        genero = self.genero_input.currentText()
        sala = self.sala_input.text()
        reservas = self.reservas_input.text()

        if not nome or not realizador or not ano or not classificacao or not sala or not reservas:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        try:
            ano = int(ano)
            classificacao = float(classificacao)
            sala = int(sala)
            reservas = int(reservas)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Ano, Classificação, Sala e Reservas devem ser números válidos.")
            return

        filme = Filme(nome, realizador, ano, classificacao, genero, sala, reservas)
        self.cinema.adicionar_filme(filme)
        self.atualizar_tabela()

    # Reserva bilhetes para o filme selecionado
    def reservar_bilhete(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Erro", "Selecione um filme para reservar bilhete.")
            return

        quantidade = self.reservar_input.text()
        if not quantidade:
            QMessageBox.warning(self, "Erro", "Digite a quantidade de bilhetes.")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            QMessageBox.warning(self, "Erro", "A quantidade de bilhetes deve ser um número válido.")
            return

        filme = self.cinema.filmes[current_row]
        if self.cinema.reservar_bilhete(filme, quantidade):
            self.atualizar_tabela()
        else:
            QMessageBox.warning(self, "Erro", "Não há bilhetes suficientes disponíveis.")

    # Remove o filme selecionado
    def remover_filme(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.cinema.remover_filme(current_row)
            self.atualizar_tabela()
        else:
            QMessageBox.warning(self, "Erro", "Selecione um filme para remover.")

    # Remove todas as reservas (define reservas para 10)
    def remover_reservas(self):
        self.cinema.remover_reservas()
        self.atualizar_tabela()

    # Carrega filmes a partir de um arquivo CSV
    def carregar_csv(self):
        csv_path, _ = QFileDialog.getOpenFileName(self, "Carregar CSV", "", "CSV Files (*.csv)")
        if csv_path:
            self.cinema.carregar_filmes(csv_path)
            self.atualizar_tabela()

    # Salva a lista de filmes em um arquivo CSV
    def salvar_csv(self):
        csv_path, _ = QFileDialog.getSaveFileName(self, "Salvar CSV", "", "CSV Files (*.csv)")
        if csv_path:
            self.cinema.salvar_filmes(csv_path)

    # Mostra um gráfico com a quantidade de bilhetes reservados por filme
    def mostrar_grafico(self):
        filmes = [filme.nome for filme in self.cinema.filmes]
        bilhetes_reservados = [10 - filme.bilhetes_disponiveis for filme in self.cinema.filmes]

        plt.bar(filmes, bilhetes_reservados)
        plt.xlabel('Filmes')
        plt.ylabel('Bilhetes Reservados')
        plt.title('Reservas de Bilhetes por Filme')
        plt.show()

# Inicializa a aplicação PyQt e a janela principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
