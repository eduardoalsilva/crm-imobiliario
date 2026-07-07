from datetime import datetime
from html import escape

import controle_envio
import database


def gerar_script_abertura_nova_aba(url: str) -> str:
    url_escapada = escape(url, quote=True)
    return (
        '<script>'
        f'window.open("{url_escapada}", "_blank", "noopener,noreferrer");'
        '</script>'
    )


def processar_abertura_whatsapp(lead_id: int, status_atual: str, callback=None) -> None:
    conn = database.conectar()

    try:
        if status_atual == "Não contatado":
            controle_envio.registrar_primeiro_contato()

        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            """
            UPDATE leads
            SET
                status = ?,
                ultimo_contato = ?
            WHERE id = ?
            """,
            ("Tentativa sem resposta", agora, lead_id),
        )
        conn.commit()
    finally:
        conn.close()

    if callback is not None:
        callback()
