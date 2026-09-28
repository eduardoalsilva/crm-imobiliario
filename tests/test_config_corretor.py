import os
import json

from config_corretor import carregar_config, salvar_config, CONFIG_PATH


def test_carregar_config_sem_arquivo_usa_padrao(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    config = carregar_config()

    assert config["nome_corretor"] == ""
    assert config["mensagem_automatica"] is True


def test_salvar_e_carregar_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    salvar_config({"nome_corretor": "Hermes", "mensagem_automatica": False})
    config = carregar_config()

    assert config["nome_corretor"] == "Hermes"
    assert config["mensagem_automatica"] is False

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        conteudo = json.load(f)
    assert conteudo["nome_corretor"] == "Hermes"