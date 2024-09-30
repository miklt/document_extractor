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


def get_prompt():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT prompt_recibo_principal FROM prompts order by data_alteracao desc limit 1"
    )
    prompt = cursor.fetchone()
    cursor.close()
    conn.close()
    return prompt


def insert_document(json_doc, comentario):    
    json_doc_str = json.dumps(json_doc)

    conn = get_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO documentos (representacao_json, cnpj, data_hora_entrega, hash_arquivo, inscricao, protocolo, tipo_entrega, validacao, comentarios)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
    """
    cursor.execute(
        insert_query,
        (
            json_doc_str,
            json_doc["cnpj"],
            json_doc["data_hora_entrega"],
            json_doc["hash_arquivo"],
            json_doc["inscricao"],
            json_doc["protocolo"],
            json_doc["tipo_entrega"],
            json_doc["validacao"],
            comentario,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()
