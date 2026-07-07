import sqlite3
from datetime import datetime, timedelta
import random

DB = "crm.db"


def conectar():
    return sqlite3.connect(DB, check_same_thread=False)


def obter_configuracao(chave):
    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        "SELECT valor FROM configuracoes WHERE chave = ?",
        (chave,)
    )

    resultado = cur.fetchone()

    conn.close()

    return resultado[0] if resultado else None


def obter_estado():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT primeiros_contatos_no_ciclo, inicio_pausa, limite_ciclo, tempo_pausa_minutos
        FROM controle_envio
        WHERE id = 1
    """)

    estado = cur.fetchone()

    conn.close()

    return estado


def obter_int_config(chave, default=0):
    valor = obter_configuracao(chave)
    return int(valor) if valor else default


def agora():
    return datetime.now()


def estado_atual():
    estado = obter_estado()

    if not estado:
        return {
            "contador": 0,
            "inicio_pausa": None,
            "limite_ciclo": None,
            "tempo_pausa_minutos": None,
        }

    contador, inicio_pausa, limite_ciclo, tempo_pausa_minutos = estado

    return {
        "contador": contador or 0,
        "inicio_pausa": inicio_pausa,
        "limite_ciclo": limite_ciclo,
        "tempo_pausa_minutos": tempo_pausa_minutos,
    }


def garantir_ciclo_inicializado():
    estado = estado_atual()

    if estado["limite_ciclo"] is None or estado["tempo_pausa_minutos"] is None:
        iniciar_novo_ciclo()
        return estado_atual()

    return estado


def esta_em_pausa():
    estado = garantir_ciclo_inicializado()

    if not estado["inicio_pausa"]:
        return False

    inicio = datetime.fromisoformat(estado["inicio_pausa"])
    tempo_maximo = timedelta(minutes=estado["tempo_pausa_minutos"])

    if agora() - inicio >= tempo_maximo:
        encerrar_pausa()
        return False

    return True


def obter_limite_ciclo():
    estado = garantir_ciclo_inicializado()
    return estado["limite_ciclo"]


def obter_tempo_pausa():
    estado = garantir_ciclo_inicializado()
    return estado["tempo_pausa_minutos"]


def sortear_limite():
    return obter_limite_ciclo()


def sortear_pausa():
    return obter_tempo_pausa()


def limite_atual():
    return obter_limite_ciclo()


def pode_enviar_primeiro_contato():
    estado = garantir_ciclo_inicializado()

    if esta_em_pausa():
        return False

    return estado["contador"] < estado["limite_ciclo"]


def registrar_primeiro_contato():
    garantir_ciclo_inicializado()

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE controle_envio
        SET primeiros_contatos_no_ciclo = primeiros_contatos_no_ciclo + 1
        WHERE id = 1
    """)

    conn.commit()
    conn.close()

    estado = estado_atual()

    if (estado["contador"] >= estado["limite_ciclo"] and not esta_em_pausa()):
        iniciar_pausa()


def reverter_primeiro_contato():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE controle_envio
        SET primeiros_contatos_no_ciclo = CASE
            WHEN primeiros_contatos_no_ciclo >= 1 THEN primeiros_contatos_no_ciclo - 1
            ELSE 0
        END
        WHERE id = 1
    """)

    conn.commit()
    conn.close()


def iniciar_novo_ciclo():
    limite = random.randint(
        obter_int_config("limite_min"),
        obter_int_config("limite_max")
    )
    tempo_pausa = random.randint(
        obter_int_config("pausa_min"),
        obter_int_config("pausa_max")
    )

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        UPDATE controle_envio
        SET
            primeiros_contatos_no_ciclo = 0,
            inicio_pausa = NULL,
            limite_ciclo = ?,
            tempo_pausa_minutos = ?
        WHERE id = 1
    """, (limite, tempo_pausa))

    conn.commit()
    conn.close()

    return {
        "limite_ciclo": limite,
        "tempo_pausa_minutos": tempo_pausa,
    }


def iniciar_pausa():
    garantir_ciclo_inicializado()

    conn = conectar()
    cur = conn.cursor()

    agora_str = agora().isoformat()

    cur.execute("""
        UPDATE controle_envio
        SET inicio_pausa = ?
        WHERE id = 1
    """, (agora_str,))

    conn.commit()
    conn.close()


def encerrar_pausa():
    iniciar_novo_ciclo()

def tempo_restante_pausa():
    estado = garantir_ciclo_inicializado()

    if not estado["inicio_pausa"]:
        return 0

    inicio = datetime.fromisoformat(estado["inicio_pausa"])
    fim = inicio + timedelta(minutes=estado["tempo_pausa_minutos"])

    restante = (fim - agora()).total_seconds()

    if restante <= 0:
        encerrar_pausa()
        return 0

    return int(restante)

