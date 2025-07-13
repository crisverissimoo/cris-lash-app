import streamlit as st
from datetime import datetime
import pytz

fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

st.set_page_config("Consultoria Cris Lash", layout="wide")

if "historico" not in st.session_state:
    st.session_state.historico = []
if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None
if "ficha_validada" not in st.session_state:
    st.session_state.ficha_validada = False
if "cliente_apta" in st.session_state and st.session_state.cliente_apta == False:
    st.error("❌ Cliente não está apta para atendimento. Reação alérgica ou condição contraindicada.")
    st.stop()

# 🌐 Idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    idioma = st.selectbox("🌐 Idioma / Language", ["Português", "Español"], key="idioma")
    def txt(pt, es): return pt if idioma == "Português" else es

    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash','Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.write(f"📅 {txt('Hoje é','Hoy es')} `{hoje.strftime('%d/%m/%Y')}`")

    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente")):
        st.markdown("<h4 style='text-align:center;'>🗂️ Cadastro da Cliente</h4>", unsafe_allow_html=True)

        nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"), key="nome_cliente")
        nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                                   min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"), key="telefone")
        email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"), key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 {txt('Idade:','Edad:')} **{idade} {txt('anos','años')}**")

        autorizada = True
        if menor:
            responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"), key="responsavel")
            autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"),
                                   ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.",
                             "❌ Cliente menor sin autorización — atención bloqueada."))
                autorizada = False

if autorizada:
    with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Ficha Clínica")):
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("<h4 style='text-align:center;'>🧾 Ficha de Anamnese Clínica</h4>", unsafe_allow_html=True)

        with st.form("form_clinica"):
            perguntas = {
                # ... suas perguntas
            }

            respostas = {}
            for chave, pergunta in perguntas.items():
                respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

            st.markdown("<br>", unsafe_allow_html=True)
            enviar = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar formulario"))
