from datetime import datetime
import unicodedata

CLASSIFICACOES = ["L", "10", "12", "14", "16", "18"]

# --- Validações ---
# Valida se a classificação indicativa é válida.
def validar_classificacao(valor):
    if valor is None:
        return None
    valor = str(valor).strip().upper()
    if valor in CLASSIFICACOES:
        return valor
    return None


# --- Entrada de dados ---
# Solicita a classificação indicativa do usuário, com validação.
def obter_classificacao(
    prompt="Classificação indicativa (L, 10, 12, 14, 16, 18): ",
    default=None, allow_blank=False
):
    while True:
        entrada = input(prompt).strip()
        if entrada == "0":
            return None
        if entrada == "" and allow_blank:
            return default
        valid = validar_classificacao(entrada)
        if valid:
            return valid
        mostrar_mensagem("erro", "Classificação inválida! Use apenas: L, 10, 12, 14, 16 ou 18.")


# Solicita uma data ao usuário, validando formato e se não está no passado.
def obter_data_valida(
    prompt="Data prevista para sair de cartaz (dd/mm/aaaa): ",
    allow_blank=False, default=None
):
    while True:
        entrada = input(prompt).strip()
        if entrada == "0":
            return None
        if entrada == "" and allow_blank:
            return default
        try:
            data_obj = datetime.strptime(entrada, "%d/%m/%Y").date()
            hoje = datetime.now().date()
            if data_obj < hoje:
                mostrar_mensagem("erro", "A data não pode ser no passado. Informe uma data igual ou posterior à de hoje.")
                continue
            return entrada  # mantém o formato dd/mm/aaaa como string
        except ValueError:
            mostrar_mensagem("erro", "Data inválida. Use o formato dd/mm/aaaa. Tente novamente.")


# Solicita ao usuário um número de sala válido (1 a 5).
def solicitar_numero_sala():
    while True:
        sala = input("Digite o número da sala (1-5 ou 0 para cancelar): ").strip()
        if sala == "0":
            return None
        if sala in [str(i) for i in range(1, 6)]:
            return sala
        mostrar_mensagem("erro", "Sala inválida. Informe um número entre 1 e 5.")

# Normaliza um texto removendo acentos e convertendo para minúsculas.
def normalizar(texto):
    if not isinstance(texto, str):
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c)
    ).lower()

# Confirma uma ação do usuário retornando True ou False.
def confirmar_acao(prompt="Tem certeza? (s/n): "):
    while True:
        r = input(prompt).strip().lower()
        if r in ("s", "sim", "y", "yes"):
            return True
        if r in ("n", "nao", "não", "no"):
            return False
        mostrar_mensagem(
            "alerta", "Resposta inválida. Digite 's' para sim ou 'n' para não."
        )


# --- Funções de exibição ---
def mostrar_mensagem(tipo, texto):
    """
    Exibe uma mensagem formatada no console.

    Parâmetros:
    tipo (str): Tipo da mensagem. Pode ser 'sucesso', 'erro', 'alerta', 'info'.
    texto (str): Conteúdo da mensagem.
    """
    icones = {
        "sucesso": "✅ ",
        "erro": "❌ ",
        "alerta": "⚠️ ",
        "info": "ℹ️ ",
    }

    icone = icones.get(tipo, "")
    print(f"{icone}{texto}")
