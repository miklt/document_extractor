import psycopg2
import streamlit as st
import json


# Function to connect to the database
def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["db_host"],
        database=st.secrets["db_name"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        port=st.secrets["db_port"],
    )
    return conn


def get_prompts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT prompt_recibo_acessorio, prompt_recibo_principal, prompt_recibo_compensacao FROM prompts order by data_alteracao desc limit 1"
    )
    prompt = cursor.fetchone()
    cursor.close()
    conn.close()
    r = None
    if prompt is not None:
        r = dict()
        r["acessorio"] = prompt[0]
        r["principal"] = prompt[1]
        r["compensacao"] = prompt[2]
    return r


# def insert_document(json_doc, comentario):
#     json_doc_str = json.dumps(json_doc)

#     conn = get_connection()
#     cursor = conn.cursor()
#     insert_query = """
#     INSERT INTO documentos (representacao_json, cnpj, data_hora_entrega, hash_arquivo, inscricao, protocolo, tipo_entrega, validacao, comentarios)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
#     """
#     cursor.execute(
#         insert_query,
#         (
#             json_doc_str,
#             json_doc["cnpj"],
#             json_doc["data_hora_entrega"],
#             json_doc["hash_arquivo"],
#             json_doc["inscricao"],
#             json_doc["protocolo"],
#             json_doc["tipo_entrega"],
#             json_doc["validacao"],
#             comentario,
#         ),
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()


def insert_document_v2(
    json_doc,
    tipo_documento,
    nome_arquivo,
    comentarios,
    escala=1,
    tokens={},
    detail="auto",
):
    json_doc_str = json.dumps(json_doc)
    tokens_str = json.dumps(tokens)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO documentos (representacao_json, tipo_documento, nome_arquivo, comentarios,escala,tokens, resolucao)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (
                json_doc_str,
                tipo_documento,
                nome_arquivo,
                comentarios,
                escala,
                tokens_str,
                detail,
            ),
        )
        conn.commit()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
