import streamlit as st
import pandas as pd
from datetime import date

import db_Cnx as db
import mdl_VarExt as mdl


# v ;;;;;;;;;;;;;;;;;;;;;;;;
# Preencher todos os clientes independente da forma d pg => obrigar TODOS os campos ?!
# No formulário em destaque se pedido ou NFe (if forma pag = TC then pedido)
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;


# ...............................................................
def Val_CnsPrecoDB(str_MercID_Pass):
    # Consulta o Preço do Produto

    str_SQL_Consulta = "SELECT val_CM06_Valor FROM Tbl_CM06_Mercadoria WHERE str_CM06_ID = " + "'" + str_MercID_Pass + "'"

    val_Preco = 0
    try:
        db.cnx_Cursor.execute(str_SQL_Consulta)
        tbl = db.cnx_Cursor.fetchall()
        val_Preco = tbl[0][0]
    except:
        pass
    finally:
        return val_Preco


# ...............................................................
def Sub_CadCli(str_Tel_Pass):
    # Consulta e Preenche os Dados do Cliente

    global str_G_Nome
    global str_G_CPF
    global str_G_Telefone
    global str_G_Endereco
    global str_G_Bairro
    global str_G_CEP
    global str_G_Municipio
    global str_G_UF
    global str_G_eMail

    if str_Tel_Pass == "NOVO":
        str_G_Nome = ""
        str_G_CPF = ""
        str_G_Telefone = ""
        str_G_Endereco = ""
        str_G_Bairro = ""
        str_G_CEP = ""
        str_G_Municipio = ""
        str_G_UF = ""
        str_G_eMail = ""
    else:
        str_SQL_Consulta = "SELECT * FROM Tbl_CC01_Conta WHERE str_CC01_Telefone = " + "'" + str_Tel_Pass + "'"

        # Consulta
        tbl_Records = []
        try:
            db.cnx_Cursor.execute(str_SQL_Consulta)
            tbl_Records = db.cnx_Cursor.fetchall()
        except:
            pass
            st.warning(f"**{'Houve um erro na busca do cliente'}**")
            return

        # Checa se o Cliente Existe e Captura os Dados
        if len(tbl_Records) == 1:
            str_G_Nome = str(tbl_Records[0][1]).strip()
            str_G_CPF = str(tbl_Records[0][2]).strip()
            str_G_Telefone = str(tbl_Records[0][3]).strip()
            str_G_Endereco = str(tbl_Records[0][5]).strip()
            str_G_Bairro = str(tbl_Records[0][6]).strip()
            str_G_CEP = str(tbl_Records[0][9]).strip()
            str_G_Municipio = str(tbl_Records[0][7]).strip()
            str_G_UF = str(tbl_Records[0][8]).strip()
            str_G_eMail = str(tbl_Records[0][4]).strip()
        else:
            st.warning(f"**{'Esse cliente não existe'}**")
            return

    str_G_Nome = str(st.text_input(label="Nome", value=str_G_Nome, key="cxt_Cli_01")).strip()
    str_G_CPF = str(st.text_input(label="CPF", value=str_G_CPF, key="cxt_Cli_02")).strip()
    str_G_Telefone = str(st.text_input(label="Telefone", value=str_G_Telefone, key="cxt_Cli_09")).strip()
    str_G_Endereco = str(st.text_input(label="Endereço", value=str_G_Endereco, key="cxt_Cli_03")).strip()
    str_G_Bairro = str(st.text_input(label="Bairro", value=str_G_Bairro, key="cxt_Cli_04")).strip()
    str_G_CEP = str(st.text_input(label="CEP", value=str_G_CEP, key="cxt_Cli_05")).strip()
    str_G_Municipio = str(st.text_input(label="Município", value=str_G_Municipio, key="cxt_Cli_06")).strip()
    str_G_UF = str(st.text_input(label="UF", value=str_G_UF, key="cxt_Cli_07")).strip()
    str_G_eMail = str(st.text_input(label="e-Mail", value=str_G_eMail, key="cxt_Cli_08")).strip()


def Sub_DataFrame():
    # Montar DataFrame

    if len(mdl.lst_Produtos) == 0:
        return

    # Monta Listas p/ DataFrame
    lst_ID = []
    for lst in mdl.lst_Produtos:
        lst_ID.append(lst[0])
    lst_Val = []
    for lst in mdl.lst_Produtos:
        lst_Val.append(str(f"{lst[1]:_.2f}".replace(".", ",").replace("_", ".")))
    lst_Qtd = []
    for lst in mdl.lst_Produtos:
        lst_Qtd.append(lst[2])

    # Show DataFrame
    mdl.pdd_DataFrame = pd.DataFrame({"ID     ": lst_ID, "Valor(R$)": lst_Val, "QTD": lst_Qtd})
    st.markdown(mdl.pdd_DataFrame.style.hide(axis="index").to_html(), unsafe_allow_html=True)


def Sub_Clear():
    # Limpa os Componentes
    st.session_state.cxt_Cli_01 = ""
    st.session_state.cxt_Cli_02 = ""
    st.session_state.cxt_Cli_03 = ""
    st.session_state.cxt_Cli_04 = ""
    st.session_state.cxt_Cli_05 = ""
    st.session_state.cxt_Cli_06 = ""
    st.session_state.cxt_Cli_07 = ""
    st.session_state.cxt_Cli_08 = ""
    st.session_state.cxt_Cli_09 = ""
    st.session_state.cxt_Prod_ID = ""
    st.session_state.cxt_Prod_Qtd = 0
    st.session_state.cxt_Rec_Desc = 0
    st.session_state.cxt_Rec_Frete = 0

    mdl.lst_Produtos = []


# ...............................................................
def Exe_Open():
    # Conectar db na Abertura - SÓ p/ CONSULTA

    bln_DB_Conectado = False
    try:
        if db.cnx_DB.is_connected():
            bln_DB_Conectado = True
    except:
        pass

    if bln_DB_Conectado is False:
        mdl.Lst_Montar()
        mdl.Pdd_Montar()
        if db.mdl_bln_db_Conectar(True) is False:
            exit(0)


def Exe_Master():
    st.set_page_config(page_title="UMK - Coletor de Vendas", page_icon="img_UMK.png")

    str_Data = date.today().strftime("%d/%m/%Y")
    st.markdown("<h4 style='text-align: center; color: grey;'>UMK - Pedido de Venda - " + str_Data + "</h4>", unsafe_allow_html=True)

    with st.form(key="key_FormVenda"):
        # Cliente
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>CLIENTE</h5>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                cmd_CliNovo = st.form_submit_button("Novo")
            with col2:
                cmd_CliBuscar = st.form_submit_button("Buscar")
            with col3:
                str_Telefone = str(
                    st.text_input(label="x", placeholder="Telefone com DDD (só números)", label_visibility="collapsed", key="cxt_Cli_Tel")
                ).strip()

            if cmd_CliNovo:
                Sub_CadCli("NOVO")

            if cmd_CliBuscar:
                if str_Telefone == "":
                    st.warning(f"**{'Digite o Telefone com DDD (só números)'}**")
                else:
                    Sub_CadCli(str_Telefone)

            st.write("---")

        # Produtos
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>PRODUTOS</h5>", unsafe_allow_html=True)

            # Campos
            col1, col2 = st.columns([1, 1])
            with col1:
                str_ProdID = str(st.text_input(label="x", placeholder="ID (código)", label_visibility="collapsed", key="cxt_Prod_ID")).strip()
            with col2:
                val_Quant = st.number_input(
                    label="x", placeholder="Quantidade", label_visibility="collapsed", format="%d", step=1, value=None, key="cxt_Prod_Qtd"
                )

            # Botões
            col1, col2 = st.columns([1, 6])
            with col1:
                cmd_ProdIncluir = st.form_submit_button("INCLUIR")
            with col2:
                cmd_ProdExcluir = st.form_submit_button("EXCLUIR")

            # Incluir Prooduto
            if cmd_ProdIncluir:
                # Buscar db
                val_Preco = Val_CnsPrecoDB(str_ProdID)
                # Checa se o Produto existe
                if val_Preco == 0:
                    st.warning(f"**{'Este produto NÃO EXISTE'}**")
                else:
                    # Checa se o Produto já consta no pedido
                    if sum(n.count(str_ProdID) for n in mdl.lst_Produtos) == 1:
                        st.warning(f"**{'Este produto JÁ CONSTA no pedido'}**")
                    else:
                        # Checa quantidade
                        if val_Quant is None or val_Quant < 0:
                            val_Quant = 1

                        # Monta Lista externa
                        mdl.lst_Produtos.extend([(str_ProdID, val_Preco, val_Quant)])

            # Excluir Produto
            if cmd_ProdExcluir:
                # Checa se o Produto existe
                if Val_CnsPrecoDB(str_ProdID) == 0:
                    st.warning(f"**{'Este produto NÃO EXISTE'}**")
                else:
                    # Checa se o Produto consta no pedido
                    if sum(n.count(str_ProdID) for n in mdl.lst_Produtos) == 0:
                        st.warning(f"**{'Este produto NÃO CONSTA no pedido'}**")
                    else:
                        # Exclui a Lista c/ o Produto e Remonta a Lista externa
                        mdl.lst_Produtos = [lst for lst in mdl.lst_Produtos if lst[0] != str_ProdID]

            # Show DataFrame
            Sub_DataFrame()

            st.write("---")

        # Recebimento
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>RECEBIMENTO</h5>", unsafe_allow_html=True)
            cbx_FormaPag = st.selectbox("Forma de Pagamento", ["Cartão", "PIX", "TC"])
            cbx_Parcelas = st.selectbox("Quantidade de Parcelas", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            val_Desconto = st.number_input(label="Desconto (R$)", step=0.5, format="%f", key="cxt_Rec_Desc")
            val_Frete = st.number_input(label="Frete / Taxas (R$)", step=0.5, format="%f", key="cxt_Rec_Frete")
            st.write("---")

        # CMD Executar
        col1, col2 = st.columns([1, 5])
        with col1:
            cmd_Executar = st.form_submit_button("EXECUTAR")
        with col2:
            st.form_submit_button("NOVO PEDIDO", on_click=Sub_Clear)
        if cmd_Executar:
            if len(mdl.lst_Produtos) > 0:
                # Calcular Total Produtos
                val_TotProd = 0
                for lst in mdl.lst_Produtos:
                    val_TotProd += lst[1] * lst[2]

                # Calcular Total NFe
                val_TotNFe = val_TotProd - val_Desconto + val_Frete

                # Formatar Saída
                str_Form = "==== Dados do Cliente ===="
                str_Form = str_Form + "\n" + "Nome: " + str_G_Nome
                str_Form = str_Form + "\n" + "CPF: " + str_G_CPF
                str_Form = str_Form + "\n" + "Telefone: " + str_G_Telefone
                str_Form = str_Form + "\n" + "Endereço: " + str_G_Endereco
                str_Form = str_Form + "\n" + "Bairro: " + str_G_Bairro
                str_Form = str_Form + "\n" + "CEP: " + str_G_CEP
                str_Form = str_Form + "\n" + "Município: " + str_G_Municipio
                str_Form = str_Form + "\n" + "UF: " + str_G_UF
                str_Form = str_Form + "\n" + "e-Mail: " + str_G_eMail

                str_Form = str_Form + "\n" + "\n" + "==== Lista de Produtos ===="
                str_Form = str_Form + "\n" + (mdl.pdd_DataFrame.to_string(index=False))
                str_Form = str_Form + "\n" + "\n" + "Total dos Produtos (R$): " + str(f"{val_TotProd:_.2f}".replace(".", ",").replace("_", "."))

                str_Form = str_Form + "\n" + "\n" + "==== Recebimento ===="
                str_Form = str_Form + "\n" + "Forma de Recebimento: " + cbx_FormaPag
                str_Form = str_Form + "\n" + "Parcelas: " + str(cbx_Parcelas)
                str_Form = str_Form + "\n" + "Desconto (R$): " + str(f"{val_Desconto:_.2f}".replace(".", ",").replace("_", "."))
                str_Form = str_Form + "\n" + "Frete / Taxas (R$): " + str(f"{val_Frete:_.2f}".replace(".", ",").replace("_", "."))
                str_Form = str_Form + "\n" + "Total da NFe (R$): " + str(f"{val_TotNFe:_.2f}".replace(".", ",").replace("_", "."))

                # Show
                st.code(str_Form)
            else:
                st.warning(f"**{'NÃO HÁ produto no pedido'}**")


# ...............................................................
Exe_Open()
Exe_Master()
