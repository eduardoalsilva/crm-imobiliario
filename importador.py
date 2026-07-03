import pandas as pd
import sqlite3

DB = "crm.db"

def importar_excel(arquivo):

    df = pd.read_excel(arquivo)
    
    if "Origem do Lead" not in df.columns:
        df["Origem do Lead"] = "Não informado"

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    for _, row in df.iterrows():

        telefone = limpar_telefone(
            row.get("Telefone", "")
        )   
        
        if not telefone:
            continue    

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
                origem_lead=?
            WHERE telefone=?
            """, (
                row.get("Nome"),
                row.get("Origem do Lead", "Não informado"),
                telefone
            ))

        else:

            cur.execute("""
            INSERT INTO leads (
                nome,
                telefone,
                whatsapp,
                origem_lead,
                status,
                interesse,
                proxima_acao,
                ultimo_contato,
                prioridade,
                observacoes
            )
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                row.get("Nome"),
                telefone,
                row.get("WhatsApp"),
                row.get("Origem do Lead", "Não informado"),
                row.get("Status") or "Não contatado",
                row.get("Interesse") or "Não definido",
                row.get("Próxima ação") or "Primeiro contato",
                row.get("Último contato"),
                row.get("Prioridade"),
                row.get("Observações")
            ))

    conn.commit()
    conn.close()

def limpar_telefone(telefone):
    telefone = str(telefone)
    return "".join(filter(str.isdigit, telefone))