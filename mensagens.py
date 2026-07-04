import json
import random
from pathlib import Path


def carregar_template(nome_template):
    caminho = Path(__file__).resolve().parent / "mensagens.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        mensagens = json.load(arquivo)

    return mensagens[nome_template]


def gerar_mensagem(lead):
    templates = [
        "primeiro_contato_1",
        "primeiro_contato_2",
        "primeiro_contato_3",
        "primeiro_contato_4"
    ]

    template_escolhido = random.choice(templates)

    texto = carregar_template(template_escolhido)

    nome = str(lead["nome"]).strip()

    primeiro_nome = nome.split()[0].capitalize()

    return texto.format(
        nome=primeiro_nome,
        corretor="Jupiter",
        empresa="Plano&Plano"
    )