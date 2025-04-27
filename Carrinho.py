import streamlit as st
import pandas as pd
import pygsheets
import datetime


credentials = st.secrets["gcp_service_account"]
gc = pygsheets.authorize(custom_credentials=credentials)

fileGoogleSheets = "https://docs.google.com/spreadsheets/d/147ck79P2FUXfcxOjqcG10HmgymQxhvoNQKOVePaB5xU"
arquivo = gc.open_by_url(fileGoogleSheets)

abaProdutos = arquivo.worksheet_by_title("Produtos")
dfProdutos = abaProdutos.get_as_df()

dfCarrinho = pd.DataFrame(columns=['Produto', 'Quantidade', 'Preço'])

# Inicializa o estado da sessão
if "cart" not in st.session_state:
    st.session_state.cart = {}

st.title("🛒 Carrinho de Compras")

# Seção para adicionar produtos
st.header("Adicionar Produto")






dfProdutosList = st.selectbox(
    'Selecione o produto',
    options=dfProdutos['Descricao'].unique()
)


dfProdutoSelecionado = dfProdutos[(dfProdutos['Descricao'] == dfProdutosList)]


product_quantity = st.number_input("Quantidade", min_value=1, step=1)

if st.button("Adicionar ao Carrinho"):
    if dfProdutosList:
        if dfProdutosList in st.session_state.cart:
            st.session_state.cart[dfProdutosList]["quantity"] += product_quantity
        else:
            st.session_state.cart[dfProdutosList] = {
                "price": float(dfProdutoSelecionado['valor'].values[0].replace(",",".")),
                "quantity": product_quantity
            }
        st.success(f"Adicionado {product_quantity} x {dfProdutosList} ao carrinho!")
    else:
        st.error("Por favor, informe o nome do produto.")

# Seção para mostrar o carrinho
st.header("🛍️ Seu Carrinho")


@st.dialog("Enviar pedido")
def enviaPedido():
    st.write(f"Preencha os dados para criação do pedido")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")
    if st.button("Enviar"):
        abaPedido = arquivo.worksheet_by_title("Pedido")
        dfPedidos = abaPedido.get_as_df()
        today = datetime.datetime.now()
        dateTimeCreate = pd.to_datetime(today)
        nPedido =len(dfPedidos)+1000
        values_list=[nPedido,str(dateTimeCreate),email,nome,telefone, total,listaItens]
        abaPedido.insert_rows(row=len(dfPedidos)+1, number=1, values=values_list)
        st.session_state.cart.clear()
        st.success(f"Pedido número [{nPedido}] enviado com sucesso!")
        st.link_button("Enviar comprovante por whatsapp", "https://streamlit.io/gallery")
        st.rerun()

if st.session_state.cart:
    listaItens = ""
    idx = 0
    for item, info in st.session_state.cart.items():
        st.write(f"**{item}** - R$ {info['price']} x {info['quantity']} unidades")
        listaItens = listaItens + f"{item} - R$ {info['price']} x {info['quantity']} unidades\n" 
        dfCarrinho.loc[idx] = [item,info['price'],info['quantity']]
        idx = idx + 1

    st.write(dfCarrinho)
    # Calcular total
    total = sum(info["price"] * info["quantity"] for info in st.session_state.cart.values())
    st.subheader(f"Total: R$ {total:.2f}")

    # Remover produto
    remove_product = st.selectbox("Remover Produto", [""] + list(st.session_state.cart.keys()))

    if st.button("Fazer pedido"):
        enviaPedido()
            

    if st.button("remover do carrinho"):
        if remove_product:
            del st.session_state.cart[remove_product]
            st.success(f"{remove_product} removido do carrinho!")

    # Botão para limpar o carrinho
    if st.button("Limpar Carrinho"):
        st.session_state.cart.clear()
        st.success("Carrinho limpo com sucesso!")
else:
    st.info("Seu carrinho está vazio.")


