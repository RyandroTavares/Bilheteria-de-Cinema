import json
from sala import Sala
from utils import (
    obter_classificacao,
    obter_data_valida,
    solicitar_numero_sala,
    confirmar_acao,
    mostrar_mensagem,
    normalizar
)

ARQUIVO_DADOS = "salas_cinema.json"

class Cinema:
    """
    Classe Cinema: gerencia salas, filmes, ingressos e persistência de dados.
    """

    def __init__(self):
        self.salas = {str(i): Sala(i) for i in range(1, 6)}

    # --- Persistência ---
    def salvar_dados(self):
        try:
            dados = {num: sala.to_dict() for num, sala in self.salas.items()}
            with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            mostrar_mensagem("erro", f"Erro ao salvar dados: {e}")

    def carregar_dados(self):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for num, info in dados.items():
                    self.salas[num] = Sala(**info)
        except FileNotFoundError:
            pass
        except Exception as e:
            mostrar_mensagem("erro", f"Erro ao carregar dados: {e}")

    # --- Funções de sistema ---
    def adicionar_filme(self, sala_num):
        sala = self.salas[sala_num]
        if sala.tem_filme():
            mostrar_mensagem("alerta", "A sala já possui um filme. Remova-o antes de adicionar outro.")
            return

        while True:
            nome = input("Nome do filme (ou 0 para cancelar): ").strip()
            if nome == "0":
                mostrar_mensagem("erro", "Operação cancelada.")
                return
            if nome == "":
                mostrar_mensagem("erro", "Nome do filme não pode ficar em branco.")
                continue
            break

        genero = input("Gênero (ou 0 para cancelar): ").strip()
        if genero == "0":
            mostrar_mensagem("erro", "Operação cancelada.")
            return
        if genero == "":
            genero = "-"

        idade = obter_classificacao()
        if idade is None:
            mostrar_mensagem("erro", "Operação cancelada.")
            return

        data_saida = obter_data_valida()
        if data_saida is None:
            mostrar_mensagem("erro", "Operação cancelada.")
            return

        sala.adicionar_filme(nome, genero, idade, data_saida)
        self.salvar_dados()
        mostrar_mensagem("sucesso", f"Filme '{nome}' adicionado à sala {sala_num} com sucesso!")

    def remover_filme(self, sala_num):
        sala = self.salas[sala_num]
        if not sala.tem_filme():
            mostrar_mensagem("alerta", "A sala já está vazia.")
            return
        
        nome = sala.filme
        if not confirmar_acao(f"Tem certeza que deseja remover o filme '{nome}' da sala {sala_num}? (s/n): "):
            mostrar_mensagem("erro", "Operação cancelada.")
            return

        sala.remover_filme()
        self.salvar_dados()
        mostrar_mensagem("sucesso", f"Filme '{nome}' removido da sala {sala_num}.")

    def atualizar_filme(self, sala_num):
        sala = self.salas[sala_num]

        if not sala.tem_filme():
            mostrar_mensagem("alerta", "Nenhum filme cadastrado nesta sala.")
            return

        print("Deixe em branco caso não queira alterar o campo.")

        nome = input(f"Novo nome do filme [{sala.filme}]: ").strip() or sala.filme
        genero = input(f"Novo gênero [{sala.genero}]: ").strip() or sala.genero

        idade = obter_classificacao(
            prompt=f"Nova classificação [{sala.idade_minima}] (L, 10, 12, 14, 16, 18): ",
            default=sala.idade_minima,
            allow_blank=True
        )
        data_saida = obter_data_valida(
            prompt=f"Nova data de saída [{sala.data_saida}] (dd/mm/aaaa) - deixe em branco para manter: ",
            allow_blank=True,
            default=sala.data_saida
        )

        sala.atualizar_filme(nome, genero, idade, data_saida)
        self.salvar_dados()
        mostrar_mensagem("sucesso", f"Dados do filme na sala {sala_num} atualizados com sucesso!")

    def emitir_ingresso(self, sala_num):
        sala = self.salas[sala_num]

        if not sala.tem_filme():
            mostrar_mensagem("alerta", "Nenhum filme em exibição nesta sala.")
            return

        while True:
            try:
                quantidade = int(input(f"Quantos ingressos deseja emitir? (Disponíveis: {sala.ingressos_disponiveis}, 0 para cancelar): "))
                if quantidade == 0:
                    mostrar_mensagem("erro", "Operação cancelada.")
                    return
                
                if quantidade < 0:
                    mostrar_mensagem("erro", "Quantidade inválida. Digite um número positivo.")
                    continue

                if not sala.emitir_ingresso(quantidade):
                    mostrar_mensagem("erro", "Ingressos insuficientes!")
                    continue
                break

            except ValueError:
                mostrar_mensagem("erro", "Digite um número válido.")

        self.salvar_dados()
        mostrar_mensagem(
            "sucesso",
            f"{quantidade} ingresso(s) emitido(s) para '{sala.filme}'. Restam {sala.ingressos_disponiveis} ingressos."
        )


    def ver_status(self):
        print("\n📊 STATUS DAS SALAS")
        for sala in self.salas.values():
            print(sala.status())

    def filtrar_filmes(self):
        while True:
            print("1. Filtrar por nome\n2. Filtrar por data de saída\n0. Cancelar")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                mostrar_mensagem("erro", "Operação cancelada.")
                return

            encontrados = []

            if opcao == "1":
                while True:
                    nome = input(
                        "Digite o nome (ou parte) do filme (0 para cancelar): "
                    ).strip()

                    if nome == "0":
                        mostrar_mensagem("erro", "Operação cancelada.")
                        return
                    
                    if not nome:
                        mostrar_mensagem("erro", "Texto de busca vazio. Digite algo ou 0 para cancelar.")
                        continue

                    nome_normalizado = normalizar(nome)  # normaliza a entrada do usuário

                    encontrados = [
                        s
                        for s in self.salas.values()
                        if normalizar(s.filme).find(nome_normalizado) != -1 and s.tem_filme()
                    ]
                    break

            elif opcao == "2":
                data = obter_data_valida(
                    prompt="Digite a data (dd/mm/aaaa) ou 0 para cancelar: ",
                    allow_blank=False
                )

                if data is None:
                    mostrar_mensagem("erro", "Operação cancelada.")
                    return
            
                encontrados = [s for s in self.salas.values() if s.data_saida == data]

            else:
                mostrar_mensagem("erro", "Opção inválida. Informe 1, 2 ou 0 para cancelar\n")
                continue

            if not encontrados:
                mostrar_mensagem("info", " Nenhum filme encontrado.")
                return

            print("\n🔎 Resultados da busca:")
            for s in encontrados:
                print(f"Sala {s.numero} — {s.filme} (Sai em: {s.data_saida})")
            return