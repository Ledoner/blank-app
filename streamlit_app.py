# streamlit_app.py

import streamlit as st
import re

st.title("🧠 Regex Substituição de Texto")

texto = st.text_area("Digite o texto de entrada:", height=200)

st.subheader("Regras Regex:")
regras = []

for i in range(5):
    col1, col2 = st.columns(2)
    with col1:
        padrao = st.text_input(f"Regex #{i+1}", key=f"regex{i}")
    with col2:
        subst = st.text_input(f"Substituir por #{i+1}", key=f"subst{i}")
    if padrao:
        regras.append((padrao, subst))

if st.button("Executar Substituição"):
    texto_resultado = texto
    for padrao, subst in regras:
        try:
            texto_resultado = re.sub(padrao, subst, texto_resultado)
        except Exception as e:
            st.error(f"Erro na regex '{padrao}': {e}")
            break
    st.subheader("Resultado:")
    st.code(texto_resultado)

if texto:
    st.download_button("📥 Baixar Resultado", texto_resultado, file_name="resultado.txt")