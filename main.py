from cinema import Cinema
from utils import solicitar_numero_sala, mostrar_mensagem

def menu():
    cinema = Cinema()
    cinema.carregar_dados()

    acoes = {
        "1": cinema.adicionar_filme,
        "2": cinema.remover_filme,
        "3": cinema.atualizar_filme,
        "4": lambda _: cinema.ver_status(),
        "5": cinema.emitir_ingresso,
        "6": lambda _: cinema.filtrar_filmes()
    }

    while True:
        print("""
==============================
🎬 BILHETERIA DO CINEMA
==============================
1. Adicionar novo filme
2. Remover filme
3. Atualizar filme
4. Ver status das salas
5. Emitir ingresso
6. Filtrar filmes
0. Sair
==============================""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            mostrar_mensagem("info", " Encerrando o sistema. Até logo! 👋")
            break

        acao = acoes.get(opcao)
        if acao:
            if opcao in ["1", "2", "3", "5"]:
                sala = solicitar_numero_sala()
                if sala is None:
                    mostrar_mensagem("erro", "Operação cancelada.")
                    continue
                acao(sala)
            else:
                acao(None)
        else:
            mostrar_mensagem("erro", "Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
