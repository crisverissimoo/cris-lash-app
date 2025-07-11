import streamlit as st
from PIL import Image
from datetime import datetime
import pytz

# 🌍 Fuso horário local
fuso_espanha = pytz.timezone("Europe/Madrid")
agora_local = datetime.now(fuso_espanha)
hoje = agora_local.date()

# 🎨 Configuração da página
st.set_page_config(page_title="Consultoria Cris Lash", layout="wide")

# 🔐 Estado da sessão
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

    # 🗂️ Cadastro da cliente
    with st.expander("🗂️ Cadastro da Cliente"):
        nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
        nascimento = st.date_input(
            "📅 Data de nascimento",
            min_value=datetime(1920, 1, 1).date(),
            max_value=hoje,
            key="nascimento"
        )
        telefone = st.text_input("📞 Telefone", key="telefone")
        email = st.text_input("📧 Email (opcional)", key="email")

        # 🧠 Cálculo de idade
        idade = hoje.year - nascimento.year - (
            (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
        )
        menor = idade < 18
        st.write(f"📌 Idade: **{idade} anos**")

        if menor:
            responsavel = st.text_input("👨‍👩‍👧 Nome do responsável", key="responsavel")
            autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error("❌ Cliente menor sem autorização — atendimento bloqueado.")
            autorizada = autorizacao == "Sim"
        else:
            autorizada = True  # Maior de idade, liberação automática

        if nascimento.month == hoje.month and nome_cliente:
            st.success(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza e carinho! 💝")
