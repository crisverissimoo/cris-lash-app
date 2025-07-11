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

    # 🗂️ Cadastro
    with st.expander("🗂️ Cadastro da Cliente"):
        nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
        nascimento = st.date_input("📅 Data de nascimento", min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input("📞 Telefone", key="telefone")
        email = st.text_input("📧 Email (opcional)", key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 Idade: **{idade} anos**")

        if menor:
            responsavel = st.text_input("👨‍👩‍👧 Nome do responsável", key="responsavel")
            autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error("❌ Cliente menor sem autorização — atendimento bloqueado.")
            autorizada = autorizacao == "Sim"
        else:
            autorizada = True

        if nascimento.month == hoje.month and nome_cliente:
            st.success(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza e carinho! 💝")

    # 🧾 Ficha Clínica
if autorizada:
    with st.expander("🧾 Ficha de Anamnese Clínica"):
        with st.form("ficha_anamnese"):
            perguntas = {
                "lentes": "Usa lentes de contato?",
                "alergia": "Tem histórico de alergias nos olhos ou pálpebras?",
                "conjuntivite": "Já teve conjuntivite nos últimos 30 dias?",
                "irritacao": "Está com olhos irritados ou lacrimejando frequentemente?",
                "gravida": "Está grávida ou amamentando?",
                "colirio": "Faz uso de colírios com frequência?",
                "infeccao": "Tem blefarite, terçol ou outras infecções oculares?",
                "cirurgia": "Fez cirurgia ocular recentemente?",
                "acido": "Está em tratamento dermatológico com ácido?",
                "sensibilidade": "Tem sensibilidade a produtos químicos ou cosméticos?",
                "extensao": "Já fez extensão de cílios antes?",
                "reacao": "Teve alguma reação alérgica em procedimentos anteriores?",
                "glaucoma": "Possui glaucoma ou outra condição ocular diagnosticada?"
            }

            respostas = {}
            for chave, pergunta in perguntas.items():
                respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

            enviar_ficha = st.form_submit_button("📨 Finalizar ficha")

            if enviar_ficha:
                if None in respostas.values():
                    st.error("⚠️ Responda todas as perguntas.")
                    st.session_state.ficha_validada = False
                else:
                    st.session_state.ficha_respostas = respostas
                    restricoes = []
                    bloqueio_total = []

                    # Lista de bloqueios críticos
                    if respostas["infeccao"] == "Sim": bloqueio_total.append("Infecção ocular ativa")
                    if respostas["conjuntivite"] == "Sim": bloqueio_total.append("Conjuntivite recente")
                    if respostas["cirurgia"] == "Sim": bloqueio_total.append("Cirurgia ocular recente")
                    if respostas["reacao"] == "Sim": bloqueio_total.append("Reação alérgica anterior")
                    if respostas["glaucoma"] == "Sim": bloqueio_total.append("Glaucoma")

                    # Alertas éticos
                    if respostas["gravida"] == "Sim":
                        st.warning("⚠️ Gestante ou lactante — recomenda-se autorização médica.")
                    if respostas["glaucoma"] == "Sim" or respostas["cirurgia"] == "Sim":
                        st.warning("⚠️ Liberação médica obrigatória.")

                    if bloqueio_total:
                        st.warning("⚠️ Cliente com restrições graves:")
                        for item in bloqueio_total:
                            st.markdown(f"- {item}")
                        st.error("❌ Cliente não apta para atendimento neste momento. Remanejar ou solicitar liberação médica.")
                        st.session_state.ficha_validada = False
                    else:
                        st.success("✅ Cliente apta para atendimento!")
                        st.session_state.ficha_validada = True

