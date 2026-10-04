import json
import unittest
from pathlib import Path
from unittest.mock import patch

from mensagens import gerar_mensagem


class MensagensTests(unittest.TestCase):
    @patch("mensagens.config_corretor.carregar_config")
    @patch("mensagens.carregar_mensagens_da_categoria")
    def test_gerar_mensagem_personaliza_nome_corretor_e_empresa(
        self, mock_mensagens, mock_config
    ):
        mock_mensagens.return_value = [
            "Olá {nome}, aqui é {corretor} da {empresa}."
        ]
        mock_config.return_value = {
            "nome_corretor": "Hermes",
            "nome_imobiliaria": "Plano&Plano",
        }

        lead = {"nome": "Maria Silva"}
        mensagem = gerar_mensagem(lead)

        self.assertIn("Maria", mensagem)
        self.assertIn("Hermes", mensagem)
        self.assertIn("Plano&Plano", mensagem)

    def test_ha_pelo_menos_1_mensagem_com_nome(self):
        caminho = Path(__file__).resolve().parents[1] / "mensagens.json"

        with open(caminho, "r", encoding="utf-8") as arquivo:
            mensagens = json.load(arquivo)

        mensagens_disponiveis = mensagens.get("primeiro_contato", [])

        self.assertGreaterEqual(len(mensagens_disponiveis), 1)

        for texto in mensagens_disponiveis:
            self.assertIn("{nome}", texto)


if __name__ == "__main__":
    unittest.main()