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


from PIL import Image  # Adicione isso no topo do seu app.py

# 💅 Consultoria e Escolha da Técnica
from PIL import Image  # Certifique-se de ter esse import no topo do app

with st.expander("👁️ Identifique o formato dos olhos da cliente"):
    st.markdown("### 📸 Exemplos de formatos de olhos")

    formato_escolhido = st.radio(
        "Qual desses formatos mais se parece com o olhar da cliente?",
        ["Pequenos", "Grandes", "Caídos", "Redondos", "Afastados", "Juntos", "Profundos"]
    )

    # Pares de exibição
    if formato_escolhido in ["Pequenos", "Grandes"]:
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://via.placeholder.com/300x200.png?text=Olhos+Pequenos", caption="Olhos Pequenos")
        with col2:
            st.image("https://via.placeholder.com/300x200.png?text=Olhos+Grandes", caption="Olhos Grandes")

    elif formato_escolhido in ["Caídos", "Redondos"]:
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://via.placeholder.com/300x200.png?text=Olhos+Ca%C3%ADdos", caption="Olhos Caídos")
        with col2:
            st.image("https://via.placeholder.com/300x200.png?text=Olhos+Redondos", caption="Olhos Redondos")

    elif formato_escolhido in ["Afastados", "Juntos"]:
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://via.placeholder.com/300x200.png?text=Olhos+Afastados", caption="Olhos Afastados")
        with col2:
            st.image("https://via.placeholder.com/300x200.png?text=Olhos+Juntos", caption="Olhos Juntos")

    elif formato_escolhido == "Profundos":
        st.image("https://via.placeholder.com/300x200.png?text=Olhos+Profundos", caption="Olhos Profundos")

    # Sugestão técnica
    sugestoes = {
        "Pequenos": "✨ Técnica indicada: **Boneca** — fios mais longos no centro para abrir o olhar.",
        "Grandes": "✨ Técnica indicada: **Gatinho ou Esquilo** — alonga e equilibra o volume.",
        "Caídos": "✨ Técnica indicada: **Esquilo** — eleva os cantos externos.",
        "Redondos": "✨ Técnica indicada: **Gatinho** — suaviza e alonga horizontalmente.",
        "Afastados": "✨ Técnica indicada: **Boneca ou Gatinho Invertido** — aproxima visualmente o olhar.",
        "Juntos": "✨ Técnica indicada: **Gatinho** — alonga os cantos externos e equilibra a distância.",
        "Profundos": "✨ Técnica indicada: **Boneca ou Gatinho** — destaca o olhar sem pesar a pálpebra."
    }

    st.info(sugestoes[formato_escolhido])


    # Simulação com foto da cliente
    st.markdown("### 📸 Simule a técnica no rosto da cliente")

    foto_cliente = st.camera_input("📷 Tire uma foto agora")
    if not foto_cliente:
        foto_cliente = st.file_uploader("Ou envie uma foto existente", type=["jpg", "jpeg", "png"])

    if foto_cliente:
        imagem = Image.open(foto_cliente)
        st.image(imagem, caption="Foto da cliente para simulação")
        st.success(f"✅ Técnica escolhida: {efeito_escolhido} — será aplicada conforme o modelo selecionado na próxima etapa.")

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
