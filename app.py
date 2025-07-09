import streamlit as st
from PIL import Image, ImageEnhance
import datetime

# Inicialização
st.set_page_config(page_title="Cris Lash Pro", layout="centered")
st.title("💻 Sistema Cris Lash")
st.markdown("### Atendimento digital completo com segurança, estilo e carinho 👑💅")

# Configurações iniciais
hoje = datetime.date.today()
if "historico" not in st.session_state:
    st.session_state.historico = []

# 🗂️ Bloco 1: Cadastro da Cliente
with st.expander("🗂️ Cadastro da Cliente"):
    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone")
    nascimento = st.date_input("📅 Data de nascimento")
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"Idade: {idade} anos")

    if nascimento.month == hoje.month and nome:
        st.success(f"🎉 Parabéns, {nome}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza, amor e cuidado! 💝\n\n🎁 Você pode ganhar um mimo especial ou uma manutenção com desconto neste atendimento.")

    if idade < 18:
        responsavel = st.text_input("Responsável (se menor)")
        st.warning("⚠️ Cliente menor de idade — exige atenção especial.")
    else:
        responsavel = ""

    autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None)

# 🧾 Bloco 2: Ficha de Anamnese
with st.form("anamnese_form"):
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
        respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None)

    if None in respostas.values():
        st.error("⚠️ Responda todas as perguntas antes de finalizar.")
        enviar_ficha = False
    else:
        enviar_ficha = st.form_submit_button("Finalizar ficha")

    if enviar_ficha:
        # Alertas de contraindicação
        if respostas["conjuntivite"] == "Sim":
            st.error("❌ Conjuntivite recente impede aplicação segura.")
        if respostas["infeccao"] == "Sim":
            st.error("❌ Infecção ocular ativa — atendimento contraindicado.")
        if respostas["cirurgia"] == "Sim":
            st.error("❌ Cirurgia ocular recente exige tempo de recuperação.")
        if respostas["reacao"] == "Sim":
            st.warning("⚠️ Histórico de reação alérgica — exigir teste prévio.")
        if respostas["glaucoma"] == "Sim":
            st.warning("⚠️ Glaucoma diagnosticado — necessário autorização médica.")

        st.success("✅ Ficha finalizada com sucesso!")

        atendimento = {
            "nome": nome,
            "telefone": telefone,
            "nascimento": nascimento,
            "idade": idade,
            "responsavel": responsavel,
            "autorizacao": autorizacao,
            "anamnese": respostas
        }
        st.session_state.historico.append(atendimento)

# 💅 Bloco 3: Escolha da Técnica
with st.expander("💅 Escolha da Técnica"):
    tecnicas = {
        "Fio a Fio": "imagens/fio_a_fio.png",
        "Volume Brasileiro": "imagens/volume_brasileiro.png",
        "Volume Russo": "imagens/volume_russo.png",
        "Híbrido": "imagens/hibrido.png",
        "Mega Volume": "imagens/mega_volume.png",
        "Efeito Delineado": "imagens/efeito_delineado.png"
    }
    tecnica_escolhida = st.selectbox("Escolha a técnica desejada", list(tecnicas.keys()))
    st.image(tecnicas[tecnica_escolhida], caption=f"Técnica: {tecnica_escolhida}")

# 🎨 Bloco 4: Simulação Visual
with st.expander("🎨 Simulação Visual"):
    st.markdown("Envie uma foto para visualizar como a técnica ficaria nos seus cílios.")
    foto = st.file_uploader("📸 Foto da cliente", type=["jpg", "jpeg", "png"])
    if foto:
        imagem = Image.open(foto)
        st.image(imagem, caption="Foto original")
        efeito = ImageEnhance.Contrast(imagem).enhance(1.4)
        st.image(efeito, caption="Foto com simulação aproximada")

# 📅 Bloco 5: Agendamento
with st.expander("📅 Agendamento"):
    data_agendamento = st.date_input("Data do atendimento", value=hoje)
    horario_opcoes = [
        "08:00", "08:30", "09:00", "09:30",
        "10:00", "10:30", "11:00", "11:30",
        "14:00", "14:30", "15:00", "15:30",
        "16:00", "16:30", "17:00", "17:30",
        "18:00", "18:30", "19:00"
    ]
    horario_escolhido = st.selectbox("Horário disponível", horario_opcoes)

# 📝 Bloco 6: Observações Extras
with st.expander("📝 Observações Extras"):
    observacoes = st.text_area("Anotações adicionais sobre o atendimento")

# 📊 Bloco 7: Histórico de Atendimento
with st.expander("📊 Histórico de Atendimento"):
    if st.session_state.historico:
        for i, registro in enumerate(st.session_state.historico):
            st.markdown(f"**{i+1}. {registro['nome']}** — {registro['idade']} anos")
            st.markdown(f"- Telefone: {registro['telefone']}")
            st.markdown(f"- Data: {registro['nascimento'].strftime('%d/%m/%Y')}")
            st.markdown(f"- Autorização: {registro['autorizacao']}")
            st.markdown(f"- Técnica: {tecnica_escolhida}")
            st.markdown(f"- Agendamento: {data_agendamento.strftime('%d/%m/%Y')} às {horario_escolhido}")
            st.markdown(f"- Observações: {observacoes}")
            st.divider()
    else:
        st.info("Nenhum atendimento registrado ainda.")

