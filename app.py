import streamlit as st
from PIL import Image, ImageEnhance
import datetime

st.set_page_config(page_title="Cris Lash Pro", layout="centered")
st.title("💻 Sistema Cris Lash")
st.markdown("### Atendimento digital completo com segurança, estilo e carinho 👑💅")

hoje = datetime.date.today()
if "historico" not in st.session_state:
    st.session_state.historico = []

## 🗂️ Cadastro da Cliente
with st.expander("🗂️ Cadastro da Cliente"):
    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone")
    nascimento = st.date_input("📅 Data de nascimento", min_value=datetime.date(1920, 1, 1), max_value=hoje)
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"Idade: {idade} anos")

    if idade < 18:
        responsavel = st.text_input("👨‍👩‍👧 Nome do responsável legal")
        autorizacao = st.radio("Autorização do responsável recebida?", ["Sim", "Não", "Pendente"], index=None)
        if autorizacao != "Sim":
            st.error("❌ Cliente menor sem autorização — atendimento não permitido.")
    else:
        responsavel = ""
        autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None)

    if nascimento.month == hoje.month and nome:
        st.success(f"🎉 Parabéns, {nome}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza, amor e cuidado! 💝")


# 🧾 Ficha de Anamnese
with st.form("ficha_anamnese"):
    st.subheader("🧾 Ficha de Anamnese Clínica")

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
        respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=chave)

    enviar_ficha = st.form_submit_button("Finalizar ficha")

    if enviar_ficha:
        if None in respostas.values():
            st.error("⚠️ Por favor, responda todas as perguntas antes de finalizar.")
        else:
            st.success("✅ Ficha finalizada com sucesso!")

            restricoes = []
            if respostas["conjuntivite"] == "Sim":
                restricoes.append("Conjuntivite recente")
            if respostas["infeccao"] == "Sim":
                restricoes.append("Infecção ocular ativa")
            if respostas["cirurgia"] == "Sim":
                restricoes.append("Cirurgia ocular recente")
            if respostas["reacao"] == "Sim":
                restricoes.append("Histórico de reação alérgica")
            if respostas["glaucoma"] == "Sim":
                restricoes.append("Glaucoma diagnosticado")
            if respostas["gravida"] == "Sim":
                st.warning("⚠️ Cliente gestante ou lactante — recomenda-se autorização médica antes do procedimento.")
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

   # 🔁 Revalidar Ficha Clínica (pós-envio)


from PIL import Image  # Certifique-se de ter esse import no topo do app

with st.expander("💅 Consultoria e Escolha da Técnica"):
    st.markdown("### 👁️ Formato dos olhos da cliente:")
    formato = st.selectbox(
        "Qual formato mais se assemelha ao olhar da cliente?",
        ["Pequenos", "Caídos", "Afastados", "Juntos", "Profundos", "Redondos"]
    )

    # Sugestão e imagem ilustrativa
    if formato == "Pequenos":
        st.image("https://via.placeholder.com/300x200?text=Olhos+Pequenos", caption="Olhos Pequenos")
        st.info("✨ Técnica recomendada: **Boneca** — fios centralizados para abrir o olhar.")
        st.markdown("💡 Curvatura: D ou CC • Comprimento: 9–13mm")

    elif formato == "Caídos":
        st.image("https://via.placeholder.com/300x200?text=Olhos+Ca%C3%ADdos", caption="Olhos Caídos")
        st.info("✨ Técnica recomendada: **Esquilo** — elevação dos cantos externos.")
        st.markdown("💡 Curvatura: C para D gradual • Evite fios longos no canto final.")

    elif formato == "Afastados":
        st.image("https://via.placeholder.com/300x200?text=Olhos+Afastados", caption="Olhos Afastados")
        st.info("✨ Técnica recomendada: **Boneca ou Gatinho Invertido** — centralização dos fios.")
        st.markdown("💡 Evite cantos externos alongados • Destaque o centro.")

    elif formato == "Juntos":
        st.image("https://via.placeholder.com/300x200?text=Olhos+Juntos", caption="Olhos Juntos")
        st.info("✨ Técnica recomendada: **Gatinho** — alonga os cantos externos.")
        st.markdown("💡 Curvatura: C • Fios curtos no canto interno.")

    elif formato == "Profundos":
        st.image("https://via.placeholder.com/300x200?text=Olhos+Profundos", caption="Olhos Profundos")
        st.info("✨ Técnica recomendada: **Boneca ou Gatinho** — destaque sem pesar a pálpebra.")
        st.markdown("💡 Curvatura: B ou C • Evite curvaturas muito intensas.")

    elif formato == "Redondos":
        st.image("https://via.placeholder.com/300x200?text=Olhos+Redondos", caption="Olhos Redondos")
        st.info("✨ Técnica recomendada: **



# 📅 Agendamento
with st.expander("📅 Agendamento"):
    data_agendamento = st.date_input("Data do atendimento", value=hoje)
    horarios_disponiveis = [
        "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
        "11:00", "11:30", "14:00", "14:30", "15:00", "15:30",
        "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00"
    ]
    horario_escolhido = st.selectbox("Horários disponíveis", horarios_disponiveis)

# 📝 Observações Extras
with st.expander("📝 Observações Extras"):
    observacoes = st.text_area("Anotações adicionais sobre a cliente ou o atendimento")

# 📊 Histórico de Atendimento
with st.expander("📊 Histórico de Atendimento"):
    st.markdown("Visualize os registros salvos abaixo:")

    if enviar_ficha:
        registro = {
            "nome": nome,
            "telefone": telefone,
            "nascimento": nascimento.strftime("%d/%m/%Y"),
            "idade": idade,
            "responsavel": responsavel,
            "autorizacao": autorizacao,
            "anamnese": respostas,
            "tecnica": tecnica_escolhida,
            "agendamento": data_agendamento.strftime("%d/%m/%Y"),
            "horario": horario_escolhido,
            "observacoes": observacoes
        }
        st.session_state.historico.append(registro)

    if st.session_state.historico:
        for i, reg in enumerate(st.session_state.historico, start=1):
            st.markdown(f"**{i}. {reg['nome']}** ({reg['idade']} anos) — {reg['agendamento']} às {reg['horario']}")
            st.markdown(f"- Técnica: {reg['tecnica']}")
            st.markdown(f"- Tel: {reg['telefone']}")
            if reg['idade'] < 18:
                st.markdown(f"🧒 Menor — Responsável: {reg['responsavel']} | Autorização: {reg['autorizacao']}")
            else:
                st.markdown(f"- Autorização: {reg['autorizacao']}")
            st.markdown(f"- Observações: {reg['observacoes']}")
            st.markdown("🧾 Anamnese:")
            for pergunta, resposta in reg['anamnese'].items():
                st.markdown(f"• {pergunta.capitalize()}: {resposta}")
            st.markdown("---")
    else:
        st.info("Nenhum atendimento registrado ainda.")
