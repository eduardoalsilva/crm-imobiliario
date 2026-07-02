import pandas as pd
import sqlite3

DB = "crm.db"

def importar_excel(arquivo):

    df = pd.read_excel(arquivo)

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    for _, row in df.iterrows():

        telefone = str(row.get("Telefone", ""))

        cur.execute(
            "SELECT id FROM leads WHERE telefone=?",
            (telefone,)
        )

        existe = cur.fetchone()

        if existe:

            cur.execute("""
            UPDATE leads
            SET
                nome=?,
                whatsapp=?,
                status=?,
                interesse=?,
                proxima_acao=?,
                ultimo_contato=?,
                prioridade=?,
                observacoes=?
            WHERE telefone=?
            """, (
                row.get("Nome"),
                row.get("WhatsApp"),
                row.get("Status"),
                row.get("Interesse"),
                row.get("Próxima ação"),
                row.get("Último contato"),
                row.get("Prioridade"),
                row.get("Observações"),
                telefone
            ))

        else:

            cur.execute("""
            INSERT INTO leads (
                nome,
                telefone,
                whatsapp,
                status,
                interesse,
                proxima_acao,
                ultimo_contato,
                prioridade,
                observacoes
            )
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                row.get("Nome"),
                telefone,
                row.get("WhatsApp"),
                row.get("Status"),
                row.get("Interesse"),
                row.get("Próxima ação"),
                row.get("Último contato"),
                row.get("Prioridade"),
                row.get("Observações")
            ))

    conn.commit()
    conn.close()