from pathlib import Path

def carregar_template(nome_template):
    caminho = Path("templates") / f"{nome_template}.txt"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def gerar_mensagem(template, lead):
    texto = carregar_template(template)

    nome = str(lead["nome"]).strip()

    primeiro_nome = nome.split()[0].capitalize()

    return texto.format(
        nome=primeiro_nome,
        corretor="Jupiter",
        empresa="Plano&Plano"
    )