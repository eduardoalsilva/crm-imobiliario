import importlib
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import Mock

import database
import controle_envio as controle_envio_module
import whatsapp_utils as whatsapp_utils_module


class WhatsappUtilsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "crm.db")

        database.DB = self.db_path
        controle_envio_module.DB = self.db_path
        whatsapp_utils_module.DB = self.db_path

        importlib.reload(database)
        importlib.reload(controle_envio_module)
        self.whatsapp_utils = importlib.reload(whatsapp_utils_module)

        database.DB = self.db_path
        controle_envio_module.DB = self.db_path
        self.whatsapp_utils.DB = self.db_path

        database.criar_banco()

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(
            "INSERT INTO leads (nome, telefone, status, ultimo_contato) VALUES (?, ?, ?, ?)",
            ("Maria", "11999999999", "Não contatado", None),
        )
        self.conn.commit()
        self.lead_id = self.conn.execute("SELECT id FROM leads WHERE nome = ?", ("Maria",)).fetchone()[0]

    def tearDown(self):
        self.conn.close()
        self.temp_dir.cleanup()

    def test_processar_abertura_whatsapp_atualiza_status_e_contato(self):
        callback = Mock()

        self.whatsapp_utils.processar_abertura_whatsapp(
            self.lead_id,
            "Não contatado",
            callback,
        )

        lead = self.conn.execute(
            "SELECT status, ultimo_contato FROM leads WHERE id = ?",
            (self.lead_id,),
        ).fetchone()

        self.assertEqual(lead[0], "Tentativa sem resposta")
        self.assertIsNotNone(lead[1])
        callback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
