import streamlit as st
import sqlite3
import pandas as pd
from urllib.parse import quote
from datetime import date

from database import criar_banco
from importador import importar_excel
from mensagens import gerar_mensagem

criar_banco()

conn = sqlite3.connect("crm.db")

st.set_page_config(
    page_title="CRM Imobiliário",
    layout="wide"
)

st.title("🏠 CRM Imobiliário")

# IMPORTAÇÃO

arquivo = st.sidebar.file_uploader(
    "Importar Excel",
    type=["xlsx"]
)

if arquivo:
    importar_excel(arquivo)
    st.success("Importação concluída")

# FILTROS

nome = st.sidebar.text_input("Buscar Nome")

telefone = st.sidebar.text_input("Buscar Telefone")

status = st.sidebar.selectbox(
    "Status",
    [
        "Todos",
        "Não contatado",
        "Tentativa sem resposta",
        "Visita",
        "Proposta",
        "Fechado",
        "Perdido"
    ]
)

query = "SELECT * FROM leads WHERE 1=1"

if nome:
    query += f" AND nome LIKE '%{nome}%'"

if telefone:
    query += f" AND telefone LIKE '%{telefone}%'"

if status != "Todos":
    query += f" AND status='{status}'"

df = pd.read_sql(query, conn)

st.subheader("Leads")

df_exibicao = df[
    [
        "id",
        "nome",
        "status",
        "ultimo_contato",
        "proxima_acao"
    ]
].copy()

df_exibicao.insert(0, "Selecionar", False)

selecionado = st.data_editor(
    df_exibicao,
    use_container_width=True,
    hide_index=True
)

linhas_selecionadas = selecionado[
    selecionado["Selecionar"] == True
]

if len(linhas_selecionadas) == 1:

    lead_id = linhas_selecionadas.iloc[0]["id"]

    st.session_state["lead_id"] = int(lead_id)

    lead = df[df["id"] == lead_id].iloc[0]

# EDIÇÃO

if "lead_id" in st.session_state:

    lead_id = st.session_state["lead_id"]

    lead_filtrado = df[df["id"] == lead_id]

    if len(lead_filtrado) == 0:
        del st.session_state["lead_id"]
        st.rerun()

    lead = lead_filtrado.iloc[0]

    with st.form("editar"):

        nome_edit = st.text_input(
            "Nome",
            lead["nome"]
        )

        status_opcoes = [
            "Não contatado",
            "Tentativa sem resposta",
            "Conversando",
            "Interessado",
            "Agendou visita",
            "Em negociação",
            "Não tem interesse",
            "Já comprou imóvel",
            "Sem Whatsapp"
        ]

        status_edit = st.selectbox(
            "Status",
            status_opcoes,
            index=status_opcoes.index(lead["status"])
            if lead["status"] in status_opcoes
            else 0
        )

        obs = st.text_area(
            "Observações",
            str(lead["observacoes"])
        )

        salvar = st.form_submit_button(
            "Salvar"
        )

        st.write("Salvar =", salvar)

    if salvar:

        conn.execute("""
        UPDATE leads
        SET
            nome=?,
            status=?,
            observacoes=?
        WHERE id=?
        """, (
            nome_edit,
            status_edit,
            obs,
            lead_id
        ))

        conn.commit()

        st.success("Atualizado")

        st.rerun()

    whatsapp = str(lead["telefone"])

    if lead["status"] == "Não contatado":
        mensagem = gerar_mensagem(
            "primeiro_contato",
            lead
        )

        url = (
            f"https://wa.me/55{whatsapp}"
            f"?text={quote(mensagem)}"
        )

    else:
        url = f"https://wa.me/55{whatsapp}"

    st.link_button(
        "📲 Abrir WhatsApp",
        url
    )