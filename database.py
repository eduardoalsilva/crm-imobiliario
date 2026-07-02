import sqlite3

DB = "crm.db"

def conectar():
    return sqlite3.connect(DB, check_same_thread=False)

def criar_banco():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        whatsapp TEXT,
        status TEXT,
        interesse TEXT,
        proxima_acao TEXT,
        ultimo_contato TEXT,
        prioridade TEXT,
        observacoes TEXT,
        data_importacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_proximo_contato DATE
    )
    """)

    conn.commit()