import streamlit as st
from PIL import Image, ImageEnhance
import datetime

st.set_page_config(page_title="Cris Lash Pro", layout="centered")
st.title("💻 Sistema Cris Lash")
st.markdown("### Atendimento digital completo com segurança, estilo e carinho 👑💅")

hoje = datetime.date.today()
if "historico" not in st.session_state:
    st.session_state.historico = []

# 🗂️ Bloco: Cadastro da Cliente
with st.expander("🗂️ Cadastro da Cliente"):
    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone")
    nascimento = st.date_input("📅 Data de nascimento", min_value=datetime.date(1920, 1, 1), max_value=hoje)
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"Valor mínimo permitido: 1920 — valor atual: {nascimento}")


    if nascimento.month == hoje.month and nome:
        st.success(f"🎉 Parabéns, {nome}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza, amor e cuidado! 💝\n\n🎁 Você pode ganhar um mimo especial ou uma manutenção com desconto neste atendimento.")

    if idade < 18:
        responsavel = st.text_input("Responsável (se menor)")
        st.warning("⚠️ Cliente menor de idade — exige atenção especial.")
    else:
        responsavel = ""

    autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None)

# 🧾 Bloco: Ficha de Anamnese
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

            # ⚠️ Lista de restrições
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

            if restricoes:
                st.warning("⚠️ Cliente com restrições — avaliar antes de prosseguir com o atendimento:")
                for item in restricoes:
                    st.markdown(f"• {item}")
            else:
                st.success("✅ Cliente apta para o procedimento! Pode seguir com a escolha da técnica e agendamento.")

            # Salva respostas no histórico
            st.session_state.ficha_respostas = respostas


# 💅 Bloco: Escolha da Técnica
with st.expander("💅 Escolha da Técnica"):
    st.markdown("Selecione a técnica desejada para visualização e agendamento.")
    tecnicas = {
        "Fio a Fio": "imagens/fio_a_fio.png",
        "Volume Brasileiro": "imagens/volume_brasileiro.png",
        "Volume Russo": "imagens/volume_russo.png",
        "Híbrido": "imagens/hibrido.png",
        "Mega Volume": "imagens/mega_volume.png",
        "Efeito Delineado": "imagens/efeito_delineado.png"
    }

    tecnica_escolhida = st.selectbox("🧵 Técnica disponível", list(tecnicas.keys()))
    imagem_técnica = tecnicas.get(tecnica_escolhida)

    try:
        st.image(imagem_técnica, caption=f"Técnica: {tecnica_escolhida}")
    except:
        st.warning("⚠️ Imagem não encontrada — verifique se está na pasta /imagens.")

# 🎨 Bloco: Simulação Visual
with st.expander("🎨 Simulação Visual"):
    st.markdown("Envie uma foto ou use a câmera para ver como a técnica ficaria em seus cílios.")

    foto = st.file_uploader("📸 Foto da cliente", type=["jpg", "jpeg", "png"])
    if foto:
        imagem = Image.open(foto)
        st.image(imagem, caption="Foto original")

        efeito = ImageEnhance.Contrast(imagem).enhance(1.3)
        st.image(efeito, caption="Foto com simulação aproximada (delineado básico)")

        st.markdown(f"🧵 Técnica selecionada: **{tecnica_escolhida}**")

# 📅 Bloco: Agendamento
with st.expander("📅 Agendamento"):
    st.markdown("Escolha a data e horário para o atendimento.")
    data_agendamento = st.date_input("Data do atendimento", value=hoje)
    horarios_disponiveis = [
        "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
        "11:00", "11:30", "14:00", "14:30", "15:00", "15:30",
        "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00"
    ]
    horario_escolhido = st.selectbox("Horários disponíveis", horarios_disponiveis)

# 📝 Bloco: Observações Extras
with st.expander("📝 Observações Extras"):
    observacoes = st.text_area("Anotações adicionais sobre a cliente ou o atendimento")

# 📊 Bloco: Histórico de Atendimento
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
            st.markdown(f"- Tel: {reg['telefone']} | Autorização: {reg['autorizacao']}")
            st.markdown(f"- Observações: {reg['observacoes']}")
            st.markdown("🧾 Anamnese:")
            for pergunta, resposta in reg['anamnese'].items():
                st.markdown(f"• {pergunta.capitalize()}: {resposta}")
            st.markdown("---")
    else:
        st.info("Nenhum atendimento registrado ainda.")
