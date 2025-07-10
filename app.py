# 📦 IMPORTS
import streamlit as st
from PIL import Image
import datetime

# 🎨 CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="Consultoria Cris Lash", layout="wide")
hoje = datetime.date.today()

# 🔐 INICIALIZA SESSION_STATE
if "historico" not in st.session_state:
    st.session_state.historico = []

if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None

if "ficha_respostas" not in st.session_state:
    st.session_state.ficha_respostas = {}

# 🎯 LAYOUT CENTRALIZADO
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 💎 Sistema de Atendimento — Cris Lash")
    st.write(f"📅 Hoje é `{hoje.strftime('%d/%m/%Y')}` — pronta pra atender com excelência!")

    # 🗂️ Cadastro da Cliente
    with st.expander("🗂️ Cadastro da Cliente"):
        st.markdown("### 📝 Informações Pessoais")

        nome_cliente = st.text_input("🧍 Nome completo da cliente", key="nome_cliente")
        nascimento = st.date_input("📅 Data de nascimento", min_value=datetime.date(1920, 1, 1), max_value=hoje, key="nascimento")
        telefone = st.text_input("📞 Telefone para contato", key="telefone")
        email = st.text_input("📧 E-mail (opcional)", key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        st.write(f"📌 Idade da cliente: **{idade} anos**")

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

    # 🧾 Ficha de Anamnese Clínica
    with st.expander("🧾 Ficha de Anamnese Clínica"):
        with st.form("ficha_anamnese"):
            st.markdown("### 🔍 Avaliação Clínica")

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
                    st.error("⚠️ Por favor, responda todas as perguntas antes de finalizar.")
                else:
                    st.success("✅ Ficha finalizada com sucesso!")

                    restricoes = []
                    if respostas["conjuntivite"] == "Sim": restricoes.append("Conjuntivite recente")
                    if respostas["infeccao"] == "Sim": restricoes.append("Infecção ocular ativa")
                    if respostas["cirurgia"] == "Sim": restricoes.append("Cirurgia ocular recente")
                    if respostas["reacao"] == "Sim": restricoes.append("Histórico de reação alérgica")
                    if respostas["glaucoma"] == "Sim": restricoes.append("Glaucoma diagnosticado")

                    if respostas["gravida"] == "Sim":
                        st.warning("⚠️ Cliente gestante ou lactante — recomenda-se autorização médica.")
                    if respostas["glaucoma"] == "Sim" or respostas["cirurgia"] == "Sim":
                        st.warning("⚠️ Este caso exige liberação médica formal — não prosseguir sem autorização documentada.")

                    if restricoes:
                        st.warning("⚠️ Cliente com restrições — avaliar antes de prosseguir:")
                        for item in restricoes:
                            st.markdown(f"• {item}")
                    elif idade < 18 and autorizacao != "Sim":
                        st.error("❌ Cliente menor sem autorização — atendimento não permitido.")
                    else:
                        st.success("✅ Cliente apta para o procedimento! Pode seguir com a escolha da técnica e agendamento.")

                    st.session_state.ficha_respostas = respostas

    # 👁️ Identificação do formato dos olhos
    with st.expander("👁️ Identifique o formato dos olhos da cliente"):
        st.markdown("### 📸 Escolha visual")

        formatos = {
            "Pequenos": "Boneca — fios longos no centro",
            "Caídos": "Esquilo — levanta canto externo",
            "Juntos": "Gatinho — alonga o canto",
            "Grandes": "Gatinho ou Esquilo — equilibra volume",
            "Redondos": "Gatinho — suaviza curvatura",
            "Afastados": "Boneca ou Gatinho Invertido — aproxima visualmente",
            "Profundos": "Boneca ou Gatinho — destaca o olhar"
        }

        for nome, tecnica in formatos.items():
            if st.button(f"👁️ Olhos {nome}", key=f"btn_{nome}"):
                st.session_state.formato_escolhido = tecnica
                st.info(f"Técnica indicada: **{tecnica}**")

        st.markdown("### 📷 Simulação com imagem da cliente")
        foto_cliente = st.camera_input("📸 Tirar foto agora")
        if not foto_cliente:
            foto_cliente = st.file_uploader("Ou envie uma foto da cliente", type=["jpg", "jpeg", "png"])

        if foto_cliente:
            imagem = Image.open(foto_cliente)
            st.image(imagem, caption="Foto da cliente")
            tecnica_final = st.session_state.formato_escolhido if st.session_state.formato_escolhido else "Não selecionado"
            st.success(f"✅ Técnica escolhida: {tecnica_final} — pronta para aplicação!")

    # 📅 Agendamento
    with st.expander("📅 Agendamento"):
        data_agendamento = st.date_input("📅 Data do atendimento", value=hoje, key="data_agendamento")
        horario_escolhido = st.selectbox("⏰ Horários disponíveis", [
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
            "11:00", "11:30", "14:00", "14:30", "15:00", "15:30",
            "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00"
        ])

    # 📝 Observações Extras
    with st.expander("📝 Observações Extras"):
        observacoes_extras = st.text_area("Anotações adicionais sobre a cliente ou atendimento", key="obs_extras")

    # 📊 Histórico de Atendimento
    with st.expander("📊 Histórico de Atendimento"):
        if enviar_ficha:
            tecnica_final = st.session_state.formato_escolhido if st.session_state.formato_escolhido else "Não selecionado"
            registro = {
                "nome": nome_cliente,
                "telefone": telefone,
                "nascimento": nascimento.strftime("%d/%m/%Y"),
                "idade": idade,
                "responsavel": responsavel,
                "autorizacao
