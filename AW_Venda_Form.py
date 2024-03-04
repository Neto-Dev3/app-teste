import streamlit as st
import pandas as pd

import db_Cnx as db
import mdl_Listas as mdl


# ...............................................................
def Tbl_Consultar(str_MercID_Pass):

    str_SQL_Consulta = (
        "SELECT"
        + " SUM(nmr_PC07_Quantidade),"
        + " str_CM06_Obs"
        + " FROM"
        + " Tbl_CM06_Mercadoria,"
        + " Tbl_PC07_Mercadoria_ES"
        + " WHERE"
        + " str_CM06_ID = FK_PC07_CM06_Mercadoria"
        + " AND str_CM06_ID = "
        + "'"
        + str_MercID_Pass
        + "'"
        + " GROUP BY str_CM06_ID"
    )

    tbl_G_Consulta = []
    try:
        db.cnx_Cursor.execute(str_SQL_Consulta)
        tbl_G_Consulta = db.cnx_Cursor.fetchall()
    except:
        pass
    finally:
        return tbl_G_Consulta


# ...............................................................
def Sub_Open():
    # Conectar db na Abertura - SÓ p/ CONSULTA

    bln_DB_Conectado = False
    try:
        if db.cnx_DB.is_connected():
            bln_DB_Conectado = True
    except:
        pass

    if bln_DB_Conectado is False:
        mdl.Lst_FormVenda()
        if db.mdl_bln_db_Conectar(True) is False:
            exit(0)


# ...............................................................
def Sub_Executar():
    st.set_page_config(page_title="UMK - Coletor de Vendas", page_icon="umk.png")
    st.markdown("<h3 style='text-align: center; color: grey;'>UMK - Coletor de Vendas </h3>", unsafe_allow_html=True)

    with st.form(key="key_FormVenda"):
        # Cliente
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>CLIENTE - NFe </h5>", unsafe_allow_html=True)
            str_Nome = st.text_input(label="Nome")
            str_CPF = st.text_input(label="CPF")
            str_Endereco = st.text_input(label="Endereço")
            str_Bairro = st.text_input(label="Bairro")
            str_CEP = st.text_input(label="CEP")
            str_Municipio = st.text_input(label="Município")
            str_UF = st.text_input(label="UF")
            st.write("---")

        # t ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        # Produtos
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>PRODUTOS </h5>", unsafe_allow_html=True)

            str_ProdID = st.text_input(label="Código do Produto")
            val_Quant = st.number_input(label="Quantidade do Produto")
            val_Valor = st.number_input(label="Valor do Produto (R$)")

            cmd_ProdIncluir = st.form_submit_button("INCLUIR")

            if cmd_ProdIncluir:

                # p
                mdl.lst_ID.append(str_ProdID)
                mdl.lst_Qtd.append(val_Quant)
                mdl.lst_Val.append(val_Valor)

                df = pd.DataFrame({"Código": mdl.lst_ID, "Quantidade": mdl.lst_Qtd, "Valor": mdl.lst_Val})

                # st.dataframe(data=df)  # Same as st.write(df)
                st.dataframe(data=df, width=600)  # Same as st.write(df)
                # st.write(df)  # Same as st.write(df)

            st.write("---")
        # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

        # Recebimento
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>RECEBIMENTO </h5>", unsafe_allow_html=True)
            cbx_FormaPag = st.selectbox("Forma de Pagamento", ["Cartão", "PIX", "TC"])
            cbx_Parcelas = st.selectbox("Quantidade de Parcelas", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            val_Desconto = st.number_input(label="Valor do Desconto (R$)")
            val_Frete = st.number_input(label="Valor do Frete (R$)")
            val_Total = st.number_input(label="Valor do Total (R$)")
            st.write("---")

        cmd_Executar = st.form_submit_button("EXECUTAR")

    # CMD Executar
    if cmd_Executar:

        # v
        # No formulário em destaque se pedido ou NFe
        # if forma pag = TC then pedido
        # if pedido não precisa preencher Cliente
        # Data Atual (Now)
        # Copiar Txt

        # t ;;;;;;;;;;;;;;;;;;;;;;;;

        st.write("Nome: ", str_Nome)
        st.write("CPF: ", str_CPF)
        st.write("Endereço: ", str_Endereco)
        st.write("Bairro: ", str_Bairro)
        st.write("CEP: ", str_CEP)
        st.write("Município: ", str_Municipio)
        st.write("UF: ", str_UF)

        st.write("Forma de Pagamento: ", cbx_FormaPag)
        st.write("Parcelas: ", cbx_Parcelas)

        st.write("Desconto: ", val_Desconto)
        st.write("Frete: ", val_Frete)
        st.write("Total: ", val_Total)

        # ..........................................

        str_Form = "Nome: " + str_Nome
        str_Form = str_Form + "\n" + "CPF: " + str_CPF
        str_Form = str_Form + "\n" + "Endereço: " + str_Endereco
        str_Form = str_Form + "\n" + "Bairro: " + str_Bairro
        str_Form = str_Form + "\n" + "CEP: " + str_CEP
        str_Form = str_Form + "\n" + "Município: " + str_Municipio
        str_Form = str_Form + "\n" + "UF: " + str_UF

        str_Form = str_Form + "\n" + "\n" + "Forma de Pagamento: " + cbx_FormaPag
        str_Form = str_Form + "\n" + "Parcelas: " + str(cbx_Parcelas)

        str_Form = str_Form + "\n" + "\n" + "Desconto (R$): " + str(f"{val_Desconto:_.2f}".replace(".", ",").replace("_", "."))
        str_Form = str_Form + "\n" + "Frete (R$): " + str(f"{val_Frete:_.2f}".replace(".", ",").replace("_", "."))
        str_Form = str_Form + "\n" + "Total (R$): " + str(f"{val_Total:_.2f}".replace(".", ",").replace("_", "."))

        st.code(str_Form)

        # ;;;;;;;;;;;;;;;;;;;;;;;;;;;


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# # Captura o ID
# str_Input = (st.text_input("Digite o CÓDIGO da mercadoria")).strip()
# if str_Input:
#     tbl_Merc = Tbl_Merc_Cns(str_Input)


# ...............................................................
Sub_Open()
Sub_Executar()
