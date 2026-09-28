import json
import os

CONFIG_PATH = "config_corretor.json"

PADRAO = {
    "nome_corretor": "",
    "mensagem_automatica": True
}


def carregar_config():
    if not os.path.exists(CONFIG_PATH):
        return PADRAO.copy()

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return {**PADRAO, **dados}


def salvar_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)