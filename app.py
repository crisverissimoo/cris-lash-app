import streamlit as st
from PIL import Image
import datetime

st.set_page_config(page_title="Consultoria Cris Lash", layout="wide")
hoje = datetime.date.today()

# Inicialização de session_state
if "historico" not in st.session_state:
    st.session_state.historico = []

if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None

if "ficha_respostas" not in st.session_state:
    st.session_state.ficha_respostas = {}

if "ficha_liberada" not in st.session_state:
    st.session_state.ficha_liberada = False

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 💎 Sistema de Atendimento — Cris Lash")
    st.write(f"📅 Hoje é `{hoje.strftime('%d/%m/%Y')}`")

    # 🗂️ Cadastro
    with st.expander("🗂️ Cadastro da Cliente"):
        nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
        nascimento = st.date_input("📅 Data de nascimento", min_value=datetime.date(1920, 1, 1), max_value=hoje, key="nascimento")
        telefone = st.text_input("📞 Telefone", key="telefone")
        email = st.text_input("📧 Email (opcional)", key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        st.write(f"📌 Idade: **{idade} anos**")

        menor = idade < 18

        if menor:
            responsavel = st.text_input("👨‍👩‍👧 Nome do responsável", key="responsavel")
            autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error("❌ Cliente menor sem autorização — atendimento bloqueado.")
        else:
            responsavel = ""
            autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_maior")

        if nascimento.month == hoje.month and nome_cliente:
            st.success(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza e carinho! 💝")

        # Liberação do fluxo
        if (not menor and autorizacao == "Sim") or (menor and autorizacao == "Sim"):
            st.session_state.ficha_liberada = True
        else:
            st.session_state.ficha_liberada = False
