# 📦 IMPORTS
import streamlit as st
from PIL import Image
from datetime import datetime
import pytz

# 🌍 AJUSTE DE FUSO HORÁRIO PARA ESPANHA
fuso_espanha = pytz.timezone("Europe/Madrid")
agora_local = datetime.now(fuso_espanha)
hoje = agora_local.date()

# 🎨 CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Consultoria Cris Lash", layout="wide")

# 🔐 SESSION STATE
if "historico" not in st.session_state:
    st.session_state.historico = []

if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None

if "ficha_respostas" not in st.session_state:
    st.session_state.ficha_respostas = {}

if "ficha_validada" not in st.session_state:
    st.session_state.ficha_validada = False

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 💎 Sistema de Atendimento — Cris Lash")
    st.write(f"📅 Hoje é `{hoje.strftime('%d/%m/%Y')}`")

    # 🗂️ Cadastro
    with st.expander("🗂️ Cadastro da Cliente"):
        nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
        nascimento = st.date_input("📅 Data de nascimento", min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input("📞 Telefone", key="telefone")
        email = st.text_input("📧 Email (opcional)", key="email")

        idade = hoje.year
