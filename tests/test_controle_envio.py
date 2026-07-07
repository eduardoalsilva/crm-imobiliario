import os
import tempfile
import unittest
from unittest.mock import patch

import importlib


class ControleEnvioTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "crm.db")

        import database
        import controle_envio as controle_envio_module

        database.DB = self.db_path
        controle_envio_module.DB = self.db_path

        importlib.reload(database)
        self.controle_envio = importlib.reload(controle_envio_module)
        self.controle_envio.DB = self.db_path
        database.conectar = lambda: self.controle_envio.conectar()

        database.criar_banco()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_iniciar_novo_ciclo_persiste_limite_e_tempo(self):
        with patch("controle_envio.random.randint", side_effect=[7, 4]):
            self.controle_envio.iniciar_novo_ciclo()

        estado = self.controle_envio.estado_atual()

        self.assertEqual(estado["limite_ciclo"], 7)
        self.assertEqual(estado["tempo_pausa_minutos"], 4)

        self.controle_envio.registrar_primeiro_contato()
        self.controle_envio.registrar_primeiro_contato()

        estado = self.controle_envio.estado_atual()

        self.assertEqual(estado["limite_ciclo"], 7)
        self.assertEqual(estado["tempo_pausa_minutos"], 4)

    def test_encerrar_pausa_reinicia_ciclo_com_novos_valores(self):
        with patch("controle_envio.random.randint", side_effect=[8, 5]):
            self.controle_envio.iniciar_novo_ciclo()

        self.controle_envio.iniciar_pausa()

        with patch("controle_envio.random.randint", side_effect=[12, 9]):
            self.controle_envio.encerrar_pausa()

        estado = self.controle_envio.estado_atual()

        self.assertEqual(estado["limite_ciclo"], 12)
        self.assertEqual(estado["tempo_pausa_minutos"], 9)
        self.assertEqual(estado["contador"], 0)
        self.assertIsNone(estado["inicio_pausa"])

    def test_reverter_primeiro_contato_desconta_tentativa(self):
        self.controle_envio.registrar_primeiro_contato()

        estado = self.controle_envio.estado_atual()
        self.assertEqual(estado["contador"], 1)

        self.controle_envio.reverter_primeiro_contato()

        estado = self.controle_envio.estado_atual()
        self.assertEqual(estado["contador"], 0)


if __name__ == "__main__":
    unittest.main()
