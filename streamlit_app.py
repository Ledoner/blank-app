import streamlit as st
import re
import json

st.set_page_config(page_title="Regex Replacer", layout="centered")
st.title("🧠 Regex Text Replacer")

# --- Initialize session state ---
if "rules" not in st.session_state:
    st.session_state.rules = [{"pattern": "", "replace": ""}]

# --- Text input ---
st.subheader("1️⃣ Texto de entrada")
upload = st.file_uploader("Ou carregue um arquivo .txt", type="txt")

if upload:
    texto = upload.read().decode("utf-8")
else:
    texto = st.text_area("Digite ou cole o texto aqui:", height=200)

# --- Add/Remove Rules ---
st.subheader("2️⃣ Regras Regex (padrão -> substituição)")

def add_rule():
    st.session_state.rules.append({"pattern": "", "replace": ""})

def remove_rule(index):
    st.session_state.rules.pop(index)

# Buttons for rule management
st.button("➕ Adicionar nova regra", on_click=add_rule)

for i, rule in enumerate(st.session_state.rules):
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        rule["pattern"] = st.text_input(f"Regex #{i+1}", value=rule["pattern"], key=f"pattern_{i}")
    with col2:
        rule["replace"] = st.text_input(f"Substituir por #{i+1}", value=rule["replace"], key=f"replace_{i}")
    with col3:
        if st.button("❌", key=f"remove_{i}"):
            remove_rule(i)
            st.experimental_rerun()

# --- Save/Load Rules as Bookmark JSON ---
st.subheader("🔖 Salvar / Carregar regras")

col_save, col_load = st.columns(2)

with col_save:
    if st.button("📥 Baixar regras"):
        rules_json = json.dumps(st.session_state.rules, indent=2, ensure_ascii=False)
        st.download_button("Salvar como JSON", data=rules_json, file_name="regras_regex.json", mime="application/json")

with col_load:
    uploaded_rules = st.file_uploader("📤 Carregar regras JSON", type="json")
    if uploaded_rules:
        try:
            new_rules = json.load(uploaded_rules)
            if isinstance(new_rules, list) and all("pattern" in r and "replace" in r for r in new_rules):
                st.session_state.rules = new_rules
                st.success("Regras carregadas com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Formato inválido de regras.")
        except Exception as e:
            st.error(f"Erro ao carregar: {e}")

# --- Execute Replacement ---
st.subheader("3️⃣ Resultado")

if st.button("🔁 Aplicar regras"):
    texto_resultado = texto
    try:
        for r in st.session_state.rules:
            texto_resultado = re.sub(r["pattern"], r["replace"], texto_resultado)
        st.text_area("Resultado final:", value=texto_resultado, height=200)
        st.download_button("📄 Baixar resultado", texto_resultado, file_name="resultado.txt")
    except re.error as e:
        st.error(f"Erro em uma regex: {e}")
else:
    st.info("Digite o texto e adicione pelo menos uma regra para aplicar.")