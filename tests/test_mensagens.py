import json
import unittest
from pathlib import Path

from mensagens import gerar_mensagem


class MensagensTests(unittest.TestCase):
    def test_gerar_mensagem_personaliza_nome_e_texto(self):
        lead = {"nome": "Maria Silva"}

        mensagem = gerar_mensagem(lead)

        self.assertIn("Maria", mensagem)
        self.assertIn("Jupiter", mensagem)
        self.assertIn("Plano&Plano", mensagem)

    def test_ha_pelo_menos_10_mensagens_com_nome(self):
        caminho = Path(__file__).resolve().parents[1] / "mensagens.json"

        with open(caminho, "r", encoding="utf-8") as arquivo:
            mensagens = json.load(arquivo)

        self.assertGreaterEqual(len(mensagens), 10)

        for texto in mensagens.values():
            self.assertIn("{nome}", texto)


if __name__ == "__main__":
    unittest.main()
