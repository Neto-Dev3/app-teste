# db cnx DEPLOY
import streamlit as st
import mysql.connector as db


def mdl_bln_db_Conectar(bln_AutoCommit_Pass):
    global cnx_DB
    global cnx_Cursor
    bln_Check = False
    try:
        cnx_DB = db.connect(
            host=st.secrets.connections.mysql.host,
            port=st.secrets.connections.mysql.port,
            user=st.secrets.connections.mysql.username,
            password=st.secrets.connections.mysql.password,
            database=st.secrets.connections.mysql.database,
            autocommit=bln_AutoCommit_Pass,
        )
        cnx_Cursor = cnx_DB.cursor()
        lst_SQL = [
            "SET interactive_timeout=28800;",
            "SET net_read_timeout=600;",
            "SET net_write_timeout=600;",
            "SET wait_timeout=28800;",
        ]
        for lst in lst_SQL:
            cnx_Cursor.execute(lst)
        if cnx_DB.is_connected():
            bln_Check = True
    except:
        pass
    finally:
        return bln_Check
