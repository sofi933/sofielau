import streamlit as st
from dados import dados

st.title("Página de Solicitação de Nome")
st.write("Esta é a segunda subpágina.")

# Campo para o usuário digitar o nome
nome = st.text_input("Digite seu nome:")

# Novo campo para o usuário digitar a idade
idade = st.number_input("Digite sua idade:", min_value=0, max_value=120, step=1)

# Se clicar no botão "Enviar"
if st.button("Enviar"):
    # Se foi preenchido o nome
    if nome:
        # Adiciona o nome e a idade informados 
        dados['Nome'].append(nome)
        dados['Idade'].append(idade)
        
        st.success(f"Olá, {nome} ({idade} anos)! Dados adicionados com sucesso.")
    else:
        st.warning("Por favor, digite seu nome antes de enviar.")

# Se clicar no botão de "Voltar"...
if st.button("Voltar ao início"):
    st.switch_page("Inicio.py")