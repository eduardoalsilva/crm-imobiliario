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


def processar_abertura_whatsapp(
    lead_id: int,
    status_atual: str,
    callback=None,
    novo_status: str = None,
    observacoes: str = None,
) -> None:
    conn = database.conectar()

    try:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if status_atual == "Não contatado":
            controle_envio.registrar_primeiro_contato()

        status_final = novo_status if novo_status is not None else (
            "Tentativa sem resposta" if status_atual == "Não contatado" else status_atual
        )

        if observacoes is not None:
            conn.execute(
                """
                UPDATE leads
                SET status = ?, ultimo_contato = ?, observacoes = ?
                WHERE id = ?
                """,
                (status_final, agora, observacoes, lead_id),
            )
        else:
            conn.execute(
                """
                UPDATE leads
                SET status = ?, ultimo_contato = ?
                WHERE id = ?
                """,
                (status_final, agora, lead_id),
            )

        conn.commit()
    finally:
        conn.close()

    if callback is not None:
        callback()
