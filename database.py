import sqlite3

DB = "crm.db"

def conectar():
    return sqlite3.connect(DB, check_same_thread=False)

def criar_tabela_configuracoes(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes (
        chave TEXT PRIMARY KEY,
        valor TEXT NOT NULL
    )
    """)

    configuracoes_padrao = [
        ("limite_min", "15"),
        ("limite_max", "30"),
        ("pausa_min", "10"),
        ("pausa_max", "20"),
    ]

    for chave, valor in configuracoes_padrao:
        cur.execute("""
        INSERT OR IGNORE INTO configuracoes (chave, valor)
        VALUES (?, ?)
        """, (chave, valor))


def criar_tabela_controle_envio(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS controle_envio (
        id INTEGER PRIMARY KEY CHECK(id = 1),
        primeiros_contatos_no_ciclo INTEGER NOT NULL DEFAULT 0,
        inicio_pausa DATETIME,
        limite_ciclo INTEGER,
        tempo_pausa_minutos INTEGER
    )
    """)

    colunas = [
        coluna[1]
        for coluna in cur.execute(
            "PRAGMA table_info(controle_envio)"
        ).fetchall()
    ]

    if "limite_ciclo" not in colunas:
        cur.execute("""
        ALTER TABLE controle_envio
        ADD COLUMN limite_ciclo INTEGER
        """)

    if "tempo_pausa_minutos" not in colunas:
        cur.execute("""
        ALTER TABLE controle_envio
        ADD COLUMN tempo_pausa_minutos INTEGER
        """)

    cur.execute("""
    INSERT OR IGNORE INTO controle_envio (
        id,
        primeiros_contatos_no_ciclo,
        inicio_pausa,
        limite_ciclo,
        tempo_pausa_minutos
    )
    VALUES (1, 0, NULL, NULL, NULL)
    """)

def executar_migracoes(cur):
    colunas = [
        coluna[1]
        for coluna in cur.execute(
            "PRAGMA table_info(leads)"
        ).fetchall()
    ]

    if "origem_lead" not in colunas:
        cur.execute("""
        ALTER TABLE leads
        ADD COLUMN origem_lead TEXT
        """)

    cur.execute("""
    UPDATE leads
    SET origem_lead = 'Não informado'
    WHERE origem_lead IS NULL
    """)

def criar_banco():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        whatsapp TEXT,
        origem_lead TEXT,
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

    cur.execute("DROP TABLE IF EXISTS logs_controle")

    executar_migracoes(cur)
    criar_tabela_configuracoes(cur)
    criar_tabela_controle_envio(cur)

    conn.commit()
    conn.close()