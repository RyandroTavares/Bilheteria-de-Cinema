class Sala:
    """
    Representa uma sala de cinema, incluindo informações sobre o filme em exibição,
    gênero, classificação indicativa, ingressos disponíveis e data de saída.
    """

    def __init__(
        self, numero, filme="Nenhum filme", genero="-", idade_minima="-",
        ingressos_disponiveis=50, data_saida="-"
    ):
        self.numero = numero
        self.filme = filme
        self.genero = genero
        self.idade_minima = idade_minima
        self.ingressos_disponiveis = ingressos_disponiveis
        self.data_saida = data_saida

    # Adiciona um filme à sala, reiniciando a quantidade de ingressos.
    def adicionar_filme(self, nome, genero, idade_minima, data_saida):
        self.filme = nome
        self.genero = genero
        self.idade_minima = idade_minima
        self.data_saida = data_saida
        self.ingressos_disponiveis = 50

    # Remove o filme atual, reiniciando os valores padrão da sala.
    def remover_filme(self):
        self.__init__(self.numero)

    # Atualiza os dados do filme, mantendo valores atuais se parâmetros forem None.
    def atualizar_filme(
        self, nome=None, genero=None, idade_minima=None, data_saida=None
    ):
        if nome is not None:
            self.filme = nome
        if genero is not None:
            self.genero = genero
        if idade_minima is not None:
            self.idade_minima = idade_minima
        if data_saida is not None:
            self.data_saida = data_saida

    # Emite um ou mais ingressos se houver disponibilidade.
    def emitir_ingresso(self, quantidade=1):
        """
        Emite a quantidade de ingressos solicitada.
        Retorna True se todos os ingressos foram emitidos, False se não houver ingressos suficientes.
        """

        if quantidade <= 0:
            return False
        
        if self.ingressos_disponiveis >= quantidade:
            self.ingressos_disponiveis -= quantidade
            return True
        return False

    # Retorna uma string formatada com o status da sala.
    def status(self):
        return f"""
-----------------------------
🎞️  Sala {self.numero}
Filme: {self.filme}
Gênero: {self.genero}
Idade mínima: {self.idade_minima}
Ingressos disponíveis: {self.ingressos_disponiveis}
Data de saída: {self.data_saida}
-----------------------------"""

    # Retorna os dados da sala em formato de dicionário para persistência.
    def to_dict(self):
        return {
            "numero": self.numero,
            "filme": self.filme,
            "genero": self.genero,
            "idade_minima": self.idade_minima,
            "ingressos_disponiveis": self.ingressos_disponiveis,
            "data_saida": self.data_saida
        }

    # Retorna True se há um filme cadastrado na sala, False caso contrário.
    def tem_filme(self):
        return self.filme != "Nenhum filme"
