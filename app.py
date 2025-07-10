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
    st.write(f"📅 Hoje é `{hoje.strftime('%d/%m/%Y')}` — atendimento com cuidado e beleza!")

    # 🗂️ Cadastro da Cliente
    with st.expander("🗂️ Cadastro da Cliente"):
        nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
        nascimento = st.date_input("📅 Data de nascimento", min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
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

    # 🧾 Ficha de Anamnese Clínica (liberada apenas se cliente autorizada)
    autorizada = (not menor and autorizacao == "Sim") or (menor and autorizacao == "Sim")
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
                        st.error("⚠️ Por favor, responda todas as perguntas.")
                        st.session_state.ficha_validada = False
                    else:
                        st.session_state.ficha_respostas = respostas
                        restricoes = []
                        if respostas["conjuntivite"] == "Sim": restricoes.append("Conjuntivite recente")
                        if respostas["infeccao"] == "Sim": restricoes.append("Infecção ocular ativa")
                        if respostas["cirurgia"] == "Sim": restricoes.append("Cirurgia ocular recente")
                        if respostas["reacao"] == "Sim": restricoes.append("Reação anterior")
                        if respostas["glaucoma"] == "Sim": restricoes.append("Glaucoma")

                        if respostas["gravida"] == "Sim":
                            st.warning("⚠️ Cliente gestante ou lactante — recomenda-se autorização médica.")
                        if respostas["glaucoma"] == "Sim" or respostas["cirurgia"] == "Sim":
                            st.warning("⚠️ Necessário liberação médica formal.")

                        if restricoes:
                            st.warning("⚠️ Cliente com restrições:")
                            for r in restricoes:
                                st.markdown(f"- {r}")
                            st.session_state.ficha_validada = False
                        else:
                            st.success("✅ Cliente apta para atendimento!")
                            st.session_state.ficha_validada = True

    # 👁️ Escolha da técnica + foto (apenas se ficha validada)
    if autorizada and st.session_state.ficha_validada:
        with st.expander("👁️ Formato dos Olhos e Foto"):
            formatos = {
                "Pequenos": "Boneca",
                "Caídos": "Esquilo",
                "Juntos": "Gatinho",
                "Grandes": "Gatinho ou Esquilo",
                "Redondos": "Gatinho",
                "Afastados": "Boneca ou Gatinho Invertido",
                "Profundos": "Boneca ou Gatinho"
            }

            for nome, tecnica in formatos.items():
                if st.button(f"👁️ Olhos {nome}", key=f"btn_{nome}"):
                    st.session_state.formato_escolhido = tecnica
                    st.info(f"Técnica indicada: **{tecnica}**")

            foto_cliente = st.camera_input("📸 Tirar foto agora")
            if not foto_cliente:
                foto_cliente = st.file_uploader("Ou envie uma foto", type=["jpg", "jpeg", "png"])

            if foto_cliente:
                imagem = Image.open(foto_cliente)
                st.image(imagem, caption="Foto da cliente")
                tecnica_final = st.session_state.formato_escolhido or "Não selecionado"
                st.success(f"✅ Técnica escolhida: {tecnica_final}")

    # 📅 Agendamento + Observações + Histórico (apenas se ficha validada)
    if autorizada and st.session_state.ficha_validada:
        with st.expander("📅 Agendamento"):
            data_agendamento = st.date_input("📅 Data", value=hoje, key="data_agendamento")
            horario = st.selectbox("⏰ Horário", [
                "08:00", "08:30", "09:00", "09:30", "10:00",
                "10:30", "11:00", "11:30", "14:00", "14:30",
                "15:00", "15:30", "16:00", "16:30", "17:00",
                "17:30", "18:00", "18:30", "19:00"
            ])

        with st.expander("📝 Observações Extras"):
            obs = st.text_area("Anotações adicionais", key="obs_extras")

        with st.expander("📊 Histórico"):
            if nome_cliente:
                registro = {
                    "nome": nome_cliente,
                    "telefone": telefone,
                    "idade": idade,
                    "formato": st.session_state.formato_escolhido,
                    "data_agendamento": data_agendamento.strftime("%d/%m/%Y"),
                    "horario": horario,
                    "observacoes": obs
                }
                st.session_state.historico.append(registro)

            if st.session_state.historico:
                for i, r in enumerate
