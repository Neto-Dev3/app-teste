import streamlit as st

# t ;;;;;;;;;;;;;;;;;;;;;;;;
import pyperclip as pclip  # Copy Cola

# ;;;;;;;;;;;;;;;;;;;;;;;;

# import db_Cnx as db


# ...............................................................
# def Sub_Open():
#     # Conectar db na Abertura - SÓ p/ CONSULTA
#     bln_DB_Conectado = False
#     try:
#         if db.cnx_DB.is_connected():
#             bln_DB_Conectado = True
#     except:
#         pass

#     if bln_DB_Conectado is False:
#         if db.mdl_bln_db_Conectar(True) is False:
#             exit(0)


def Sub_Executar():
    st.set_page_config(page_title="UMK - Coletor de Vendas", page_icon="umk.png")
    st.markdown("<h3 style='text-align: center; color: grey;'>UMK - Coletor de Vendas </h3>", unsafe_allow_html=True)

    with st.form(key="key_FormVenda"):
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

        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>RECEBIMENTO </h5>", unsafe_allow_html=True)
            cbx_FormaPag = st.selectbox("Forma de Pagamento", ["Cartão", "PIX", "TC"])
            cbx_Parcelas = st.selectbox("Quantidade de Parcelas", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            st.write("---")

        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>VALORES </h5>", unsafe_allow_html=True)
            val_Desconto = st.number_input(label="Valor do Desconto")
            val_Frete = st.number_input(label="Valor do Frete")
            val_Total = st.number_input(label="Valor do Total")
            st.write("---")

        cmd_Executar = st.form_submit_button("Executar")

    # CMD Executar
    if cmd_Executar:

        # v
        # No formulário em destaque se pedido ou NF
        # Data Atual (Now)
        # Copiar Txt

        # p ;;;;;;;;;;;;;;;;;;;;;;;;

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

        pclip.copy(str_Nome)
        # ;;;;;;;;;;;;;;;;;;;;;;;;;;;


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# # Captura o ID
# str_Input = (st.text_input("Digite o CÓDIGO da mercadoria")).strip()
# if str_Input:
#     tbl_Merc = Tbl_Merc_Cns(str_Input)

#     # Checa se a Mercadoria existe e se tem Estoque
#     if len(tbl_Merc) == 0:
#         st.write("Esta mercadoria NÃO EXISTE")
#     else:
#         val_Estoque = tbl_Merc[0][0]
#         if val_Estoque == 0:
#             st.write("Esta mercadoria está SEM ESTOQUE")
#         else:
#             st.write("Estoque: ", val_Estoque)
#             st.write(tbl_Merc[0][1])


# ...............................................................
# Sub_Open()
Sub_Executar()
