from pathlib import Path
import random

def carregar_template(nome_template):
    caminho = Path("templates") / f"{nome_template}.txt"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


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