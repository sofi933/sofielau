# 3_Celular.py
import streamlit as st
from dados import dados_celulares

st.title("Cadastro e Listagem de Celulares")
st.write("Nesta página você pode cadastrar e visualizar as informações de telefones celulares.")

st.subheader("Informe os dados do celular")

# Campos de entrada de dados
numero = st.text_input("Número do celular:")
marca = st.text_input("Marca:")
modelo = st.text_input("Modelo:")
operadora = st.selectbox("Operadora do chip:", ["Vivo", "Claro", "TIM", "Outra"])

# Botão para salvar
if st.button("Salvar Celular"):
    if numero and marca and modelo:
        # Adiciona os valores informados nas listas do dicionário
        dados_celulares["Número"].append(numero)
        dados_celulares["Marca"].append(marca)
        dados_celulares["Modelo"].append(modelo)
        dados_celulares["Operadora"].append(operadora)
        
        st.success("Celular cadastrado com sucesso!")
    else:
        st.warning("Por favor, preencha os campos obrigatórios (Número, Marca e Modelo).")

# Exibição dos dados em formato tabular na mesma página
st.subheader("Tabela de Celulares Cadastrados")
st.dataframe(dados_celulares)

# Botão para voltar ao início
if st.button("Voltar ao início"):
    st.switch_page("Inicio.py")