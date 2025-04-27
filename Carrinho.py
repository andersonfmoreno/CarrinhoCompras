import streamlit as st

# Inicializa o estado da sessão
if "cart" not in st.session_state:
    st.session_state.cart = {}

st.title("🛒 Carrinho de Compras")

# Seção para adicionar produtos
st.header("Adicionar Produto")

product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
product_quantity = st.number_input("Quantidade", min_value=1, step=1)

if st.button("Adicionar ao Carrinho"):
    if product_name:
        if product_name in st.session_state.cart:
            st.session_state.cart[product_name]["quantity"] += product_quantity
        else:
            st.session_state.cart[product_name] = {
                "price": product_price,
                "quantity": product_quantity
            }
        st.success(f"Adicionado {product_quantity}x {product_name} ao carrinho!")
    else:
        st.error("Por favor, informe o nome do produto.")

# Seção para mostrar o carrinho
st.header("🛍️ Seu Carrinho")

if st.session_state.cart:
    for item, info in st.session_state.cart.items():
        st.write(f"**{item}** - R$ {info['price']:.2f} x {info['quantity']} unidades")

    # Calcular total
    total = sum(info["price"] * info["quantity"] for info in st.session_state.cart.values())
    st.subheader(f"Total: R$ {total:.2f}")

    # Remover produto
    remove_product = st.selectbox("Remover Produto", [""] + list(st.session_state.cart.keys()))
    if st.button("Remover"):
        if remove_product:
            del st.session_state.cart[remove_product]
            st.success(f"{remove_product} removido do carrinho!")
else:
    st.info("Seu carrinho está vazio.")

# Botão para limpar o carrinho
if st.button("Limpar Carrinho"):
    st.session_state.cart.clear()
    st.success("Carrinho limpo com sucesso!")
