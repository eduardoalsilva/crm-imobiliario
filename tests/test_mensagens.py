import unittest

from mensagens import gerar_mensagem


class MensagensTests(unittest.TestCase):
    def test_gerar_mensagem_personaliza_nome_e_texto(self):
        lead = {"nome": "Maria Silva"}

        mensagem = gerar_mensagem(lead)

        self.assertIn("Maria", mensagem)
        self.assertIn("Jupiter", mensagem)
        self.assertIn("Plano&Plano", mensagem)


if __name__ == "__main__":
    unittest.main()
