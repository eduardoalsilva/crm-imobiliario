import streamlit as st
import sqlite3
import pandas as pd
from urllib.parse import quote
from datetime import datetime
from config_corretor import carregar_config, salvar_config
import database

from database import criar_banco, conectar
from importador import importar_excel
from mensagens import gerar_mensagem
from whatsapp_utils import processar_abertura_whatsapp
from controle_envio import (
    pode_enviar_primeiro_contato,
    registrar_primeiro_contato,
    reverter_primeiro_contato,
    esta_em_pausa,
    estado_atual,
    obter_limite_ciclo,
    tempo_restante_pausa,
)



criar_banco()

conn = sqlite3.connect("crm.db")

@st.dialog("Ligar")
def dialog_ligar():
    conn_dialog = conectar()

    fila = st.session_state.get("fila_ligar", [])
    posicao = st.session_state.get("posicao_ligar", 0)

    if posicao >= len(fila):
        st.success(f"Fila concluída — {len(fila)} leads processados.")
        if st.button("Fechar"):
            st.session_state["mostrar_dialog_ligar"] = False
            conn_dialog.close()
            st.rerun()
        conn_dialog.close()
        return

    lead_id = fila[posicao]
    cur = conn_dialog.cursor()
    cur.execute(
        "SELECT nome, telefone, status, observacoes FROM leads WHERE id = ?",
        (lead_id,)
    )
    resultado = cur.fetchone()

    if resultado is None:
        conn_dialog.close()
        st.session_state["posicao_ligar"] += 1
        st.rerun()
        return

    nome, telefone, status_atual, observacoes_atual = resultado

    st.caption(f"{posicao + 1} de {len(fila)}")
    contador = st.session_state.get("contador_ligacoes", 0)
    cor_bolinha = "🟢" if contador >= 40 else "🔴"

    st.write(f"{cor_bolinha} **{contador} / 40** ligações nesta sessão")
    st.subheader(nome or "(sem nome)")
    st.write(f"📞 {telefone}")

    obs_input = st.text_area(
        "Observações",
        value=observacoes_atual or "",
        key=f"obs_ligar_{lead_id}"
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

    status_padrao = (
        "Tentativa sem resposta"
        if status_atual == "Não contatado"
        else status_atual
    )

    status_input = st.selectbox(
        "Status",
        status_opcoes,
        index=status_opcoes.index(status_padrao) if status_padrao in status_opcoes else 0,
        key=f"status_ligar_{lead_id}"
    )

    config = carregar_config()

    mensagem_automatica_input = st.checkbox(
        "Mensagem automática",
        value=config["mensagem_automatica"],
        key=f"msg_auto_{lead_id}"
    )

    if mensagem_automatica_input != config["mensagem_automatica"]:
        config["mensagem_automatica"] = mensagem_automatica_input
        salvar_config(config)

    em_pausa = esta_em_pausa()
    pode_enviar = pode_enviar_primeiro_contato()
    estado = estado_atual()
    limite = obter_limite_ciclo()

    if em_pausa:
        restante = tempo_restante_pausa()
        minutos, segundos = restante // 60, restante % 60
        st.error(f"⛔ Pausa ativa — libera em {minutos:02d}:{segundos:02d}")
    else:
        st.success("🟢 Envio liberado")

    st.caption(f"📊 Ciclo atual: {estado['contador']} / {limite}")

    if mensagem_automatica_input:
        mensagem = gerar_mensagem({"nome": nome})
        url = f"https://wa.me/55{telefone}?text={quote(mensagem)}"
    else:
        url = f"https://wa.me/55{telefone}"

    col1, col2 = st.columns(2)

    if em_pausa or not pode_enviar:
        col1.button("📲 WhatsApp (bloqueado)", disabled=True, use_container_width=True)
    else:
        col1.link_button(
            "📲 Abrir WhatsApp",
            url,
            on_click=processar_abertura_whatsapp,
            kwargs={
                "lead_id": lead_id,
                "status_atual": status_atual,
                "novo_status": status_input,
                "observacoes": obs_input,
            },
            type="primary",
            use_container_width=True,
        )

    if col2.button("➡️ Próximo", use_container_width=True):
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn_dialog.execute(
            "UPDATE leads SET status=?, ultimo_contato=?, observacoes=? WHERE id=?",
            (status_input, agora, obs_input, lead_id)
        )
        conn_dialog.commit()
        conn_dialog.close()
        st.session_state["posicao_ligar"] += 1
        st.session_state["contador_ligacoes"] = st.session_state.get("contador_ligacoes", 0) + 1
        st.rerun()

    if st.button("✖ Fechar", use_container_width=True):
        conn_dialog.close()
        st.session_state["mostrar_dialog_ligar"] = False
        st.session_state["contador_ligacoes"] = 0
        st.rerun()

if st.session_state.get("mostrar_dialog_ligar"):
    dialog_ligar()

st.set_page_config(
    page_title="CRM Imobiliário",
    layout="wide"
)

st.title("🏠 CRM Imobiliário")

config = carregar_config()

nome_corretor_input = st.sidebar.text_input(
    "Corretor",
    config["nome_corretor"]
)

if nome_corretor_input != config["nome_corretor"]:
    config["nome_corretor"] = nome_corretor_input
    salvar_config(config)

nome_imobiliaria_input = st.sidebar.text_input(
    "Imobiliária",
    config["nome_imobiliaria"]
)

if nome_imobiliaria_input != config["nome_imobiliaria"]:
    config["nome_imobiliaria"] = nome_imobiliaria_input
    salvar_config(config)

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

origem = st.sidebar.text_input(
    "Origem do Lead"
)

status = st.sidebar.selectbox(
    "Status",
    [
    "Todos",
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
)

query = "SELECT * FROM leads WHERE 1=1"

if nome:
    query += f" AND nome LIKE '%{nome}%'"

if telefone:
    query += f" AND telefone LIKE '%{telefone}%'"

if origem:
    query += f" AND origem_lead LIKE '%{origem}%'"

if status != "Todos":
    query += f" AND status='{status}'"

df = pd.read_sql(query, conn)

st.subheader(f"Leads ({len(df)})")

if st.button("📞 Ligar", disabled=df.empty):
    st.session_state["fila_ligar"] = df["id"].tolist()
    st.session_state["posicao_ligar"] = 0
    st.session_state["contador_ligacoes"] = 0
    st.session_state["mostrar_dialog_ligar"] = True

df_exibicao = df[
    [
        "id",
        "nome",
        "telefone",
        "origem_lead",
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

        #origem_edit = st.text_input(
         #   "Origem do Lead",
          #  str(lead["origem_lead"])
        #)

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

    if salvar:
        if status_edit == "Sem Whatsapp" and lead["status"] != "Sem Whatsapp":
            reverter_primeiro_contato()

        conn.execute("""
        UPDATE leads
        SET
            nome=?,
            
            status=?,
            observacoes=?
        WHERE id=?
        """, (
            nome_edit,
            # origem_edit,
            status_edit,
            obs,
            lead_id
        ))

        conn.commit()

        st.success("Atualizado")

        st.rerun()

    # whatsapp = str(lead["telefone"])

    # if lead["status"] == "Não contatado":
    #     mensagem = gerar_mensagem(lead)

    #     url = (
    #         f"https://wa.me/55{whatsapp}"
    #         f"?text={quote(mensagem)}"
    #     )

    # else:
    #     url = f"https://wa.me/55{whatsapp}"

    # estado = estado_atual()

    # em_pausa = esta_em_pausa()
    # pode_enviar = pode_enviar_primeiro_contato()

    # contador = estado["contador"]

    # limite = obter_limite_ciclo()

    # if em_pausa:
    #     restante = tempo_restante_pausa()
    #     minutos = restante // 60
    #     segundos = restante % 60

    #     st.error(f"⛔ Pausa ativa — libera em {minutos:02d}:{segundos:02d}")
    # else:
    #     st.success("🟢 Envio liberado")

    # st.caption(f"📊 Ciclo atual: {contador} / {limite}")

    # if em_pausa or not pode_enviar:
    #     st.button("📲 Abrir WhatsApp (bloqueado)", disabled=True)

    # else:
    #     st.link_button(
    #         "📲 Abrir WhatsApp",
    #         url,
    #         on_click=processar_abertura_whatsapp,
    #         args=(lead_id, lead["status"]),
    #         type="primary",
    #     )