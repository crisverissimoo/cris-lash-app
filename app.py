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

with st.expander("🗂️ Cadastro da Cliente"):
    st.markdown("### 📝 Informações Pessoais")

    nome_cliente = st.text_input("🧍 Nome completo da cliente", key="nome_cliente")
    nascimento = st.date_input("📅 Data de nascimento", min_value=datetime.date(1920, 1, 1), max_value=hoje, key="nascimento")
    telefone = st.text_input("📞 Telefone para contato", key="telefone")
    email = st.text_input("📧 E-mail (opcional)", key="email")

    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"📌 Idade da cliente: **{idade} anos**")

    st.markdown("### 🌟 Preferências")
    primeira_vez = st.radio("É a primeira vez que faz alongamento de cílios?", ["Sim", "Não"], key="primeira_vez")
    if primeira_vez == "Não":
        st.text_input("Qual técnica já usou anteriormente?", key="tecnica_usada")

    if idade < 18:
        responsavel = st.text_input("👨‍👩‍👧 Nome do responsável legal", key="responsavel")
        autorizacao = st.radio("Autorização do responsável recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
        if autorizacao != "Sim":
            st.error("❌ Cliente menor sem autorização — atendimento não permitido.")
    else:
        responsavel = ""
        autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_maior")

    if nascimento.month == hoje.month and nome_cliente:
        st.success(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza, amor e cuidado! 💝")
