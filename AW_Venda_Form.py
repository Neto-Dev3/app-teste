import streamlit as st
import pandas as pd

import db_Cnx as db
import mdl_VarExt as mdl


# ...............................................................
def Tbl_Consultar(str_MercID_Pass):
    # Consulta o Preço do Produto

    str_SQL_Consulta = "SELECT" + " val_CM06_Valor" + " FROM" + " Tbl_CM06_Mercadoria" + " WHERE" + " str_CM06_ID = " + "'" + str_MercID_Pass + "'"

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
def Sub_Open():
    # Conectar db na Abertura - SÓ p/ CONSULTA

    bln_DB_Conectado = False
    try:
        if db.cnx_DB.is_connected():
            bln_DB_Conectado = True
    except:
        pass

    if bln_DB_Conectado is False:
        mdl.Lst_Montar()
        if db.mdl_bln_db_Conectar(True) is False:
            exit(0)


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
            str_eMail = st.text_input(label="e-Mail")
            st.write("---")

        # Produtos
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>PRODUTOS </h5>", unsafe_allow_html=True)

            # p ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
            # str_ProdID = st.text_input(label="Código do Produto")
            # val_Quant = st.number_input(label="Quantidade do Produto", format="%d", step=1, value=1)

            col1, col2 = st.columns([1, 1])
            with col1:
                str_ProdID = st.text_input(label="", placeholder="ID (código)", label_visibility="collapsed")
            with col2:
                val_Quant = st.number_input(label="", placeholder="Quantidade", label_visibility="collapsed", format="%d", step=1, value=None)
            # ....................................................................

            # col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            # with col1:
            #     str_ProdID = st.text_input(label="", placeholder="ID (código)", label_visibility="collapsed")
            # with col2:
            #     val_Quant = st.number_input(label="", placeholder="Quantidade", label_visibility="collapsed", format="%d", step=1, value=None)
            # with col3:
            #     cmd_ProdIncluir = st.form_submit_button("INCLUIR")
            # with col4:
            #     cmd_ProdExcluir = st.form_submit_button("EXCLUIR")

            # ....................................................................

            col1, col2 = st.columns([1, 6])
            with col1:
                cmd_ProdIncluir = st.form_submit_button("INCLUIR")
            with col2:
                cmd_ProdExcluir = st.form_submit_button("EXCLUIR")

            # cmd_ProdIncluir = st.form_submit_button("INCLUIR")
            # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

            # Incluir Prooduto
            if cmd_ProdIncluir:
                # Buscar db
                val_Preco = Tbl_Consultar(str_ProdID)
                # Checa se a Mercadoria existe
                if val_Preco == 0:
                    st.write(f"**{'Este produto NÃO EXISTE'}**")
                else:
                    # Monta Lista externa
                    mdl.lst_Produtos.extend([(str_ProdID, val_Quant, val_Preco)])

                    # Monta Listas p/ DataFrame
                    lst_ID = []
                    for lst in mdl.lst_Produtos:
                        lst_ID.append(lst[0])
                    lst_Qtd = []
                    for lst in mdl.lst_Produtos:
                        lst_Qtd.append(lst[1])
                    lst_Val = []
                    for lst in mdl.lst_Produtos:
                        lst_Val.append(str(f"{lst[2]:_.2f}".replace(".", ",").replace("_", ".")))

                    # p ;;;;;;;;;;;;;;;;;;;;;;;;
                    # Show DataFrame
                    df = pd.DataFrame({"Código": lst_ID, "Quantidade": lst_Qtd, "Valor": lst_Val})
                    # st.table(df)

                    # Remove index
                    # st.dataframe(df, hide_index=True)
                    # st.table(df.assign(hack='').set_index('hack'))

                    st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                    # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

            # p ;;;;;;;;;;;;;;;;;;;;;;;;
            # Opção Deletar item

            # Excluir Prooduto
            if cmd_ProdExcluir:
                mdl.lst_Produtos.remove("H01VCJ230901")
            # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

            st.write("---")

        # Recebimento
        with st.container():
            st.markdown("<h5 style='text-align: center; color: grey;'>RECEBIMENTO </h5>", unsafe_allow_html=True)
            cbx_FormaPag = st.selectbox("Forma de Pagamento", ["Cartão", "PIX", "TC"])
            cbx_Parcelas = st.selectbox("Quantidade de Parcelas", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            val_Desconto = st.number_input(label="Valor do Desconto (R$)", step=0.5, format="%f")
            val_Frete = st.number_input(label="Valor do Frete (R$)", step=0.5, format="%f")

            st.write("---")

        cmd_Executar = st.form_submit_button("EXECUTAR")

    # CMD Executar
    if cmd_Executar:

        # v ;;;;;;;;;;;;;;;;;;;;;;;;
        # Data Atual (Now)
        # Preencher todos os clientes independente da forma d pg => obrigar !
        # Buscar db clientes pré existentes
        # No formulário em destaque se pedido ou NFe (if forma pag = TC then pedido)
        # ;;;;;;;;;;;;;;;;;;;;;;;;;;;

        # Calcular Total Produtos
        val_TotProd = 0
        for lst in mdl.lst_Produtos:
            val_TotProd += lst[1] * lst[2]

        # Calcular Total NFe
        val_TotNFe = val_TotProd - val_Desconto + val_Frete

        # Formatar Saída
        str_Form = "============ Dados do Cliente ============"
        str_Form = str_Form + "\n" + "Nome: " + str_Nome
        str_Form = str_Form + "\n" + "CPF: " + str_CPF
        str_Form = str_Form + "\n" + "Endereço: " + str_Endereco
        str_Form = str_Form + "\n" + "Bairro: " + str_Bairro
        str_Form = str_Form + "\n" + "CEP: " + str_CEP
        str_Form = str_Form + "\n" + "Município: " + str_Municipio
        str_Form = str_Form + "\n" + "UF: " + str_UF
        str_Form = str_Form + "\n" + "e-Mail: " + str_eMail

        str_Form = str_Form + "\n" + "\n" + "============ Lista de Produtos ============"
        str_ID = "Código: "
        str_Qtd = "Quantidade: "
        str_Val = "Preço: "
        for lst in mdl.lst_Produtos:
            str_Produto = (
                str_ID + lst[0] + " | " + str_Qtd + str(lst[1]) + " | " + str_Val + str(f"{lst[2]:_.2f}".replace(".", ",").replace("_", "."))
            )
            str_Form = str_Form + "\n" + str_Produto

        str_Form = str_Form + "\n" + "\n" + "============ Recebimento ============"
        str_Form = str_Form + "\n" + "Forma de Recebimento: " + cbx_FormaPag
        str_Form = str_Form + "\n" + "Parcelas: " + str(cbx_Parcelas)
        str_Form = str_Form + "\n" + "Desconto (R$): " + str(f"{val_Desconto:_.2f}".replace(".", ",").replace("_", "."))
        str_Form = str_Form + "\n" + "Frete / Despesas Acessórias (R$): " + str(f"{val_Frete:_.2f}".replace(".", ",").replace("_", "."))

        str_Form = str_Form + "\n" + "\n" + "============ Fechamento ============"
        str_Form = str_Form + "\n" + "\n" + "Total dos Produtos (R$): " + str(f"{val_TotProd:_.2f}".replace(".", ",").replace("_", "."))
        str_Form = str_Form + "\n" + "Total da NFe (R$): " + str(f"{val_TotNFe:_.2f}".replace(".", ",").replace("_", "."))

        # Show
        st.code(str_Form)


# ...............................................................
Sub_Open()
Sub_Executar()
