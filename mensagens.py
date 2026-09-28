import json
import random
from pathlib import Path


def carregar_mensagens():
    caminho = Path(__file__).resolve().parent / "mensagens.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def carregar_mensagens_da_categoria(categoria="primeiro_contato"):
    mensagens_por_categoria = carregar_mensagens()
    return mensagens_por_categoria[categoria]


def gerar_mensagem(lead):
    mensagens = carregar_mensagens_da_categoria()
    texto = random.choice(mensagens)

    nome = str(lead["nome"]).strip()

    primeiro_nome = nome.split()[0].capitalize()

    return texto.format(
        nome=primeiro_nome,
        corretor="Hermes",
        empresa="Plano&Plano"
    )