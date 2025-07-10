# 📦 IMPORTS
import streamlit as st
from PIL import Image
import datetime

# 🎨 CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Consultoria Lash", layout="wide")
hoje = datetime.date.today()

# 🔐 INICIALIZA SESSION_STATE
if "historico" not in st.session_state:
    st.session_state.historico = []

if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None

if "ficha_respostas" not in st.session_state:
    st.session_state.ficha_respostas = {}

# 🎯 INÍCIO DO LAYOUT CENTRALIZADO
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 💎 Sistema de Atendimento — Cris Lash")
    st.write(f"📅 Hoje é `{hoje.strftime('%d/%m/%Y')}` — pronta pra atender com excelência!")
