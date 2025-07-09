import streamlit as st
from PIL import Image, ImageEnhance
import datetime

# Textos
txt = {
    "cadastro": "🗂️ Cadastro da Cliente",
    "nome": "Nome completo",
    "telefone": "Telefone",
    "nascimento": "Data de nascimento",
    "idade": "Idade calculada",
    "responsavel": "Responsável (se menor)",
    "autorizacao": "Autorização recebida?",
    "alerta_menor": "Cliente menor de idade — exige atenção especial.",
    "aniversario": "🎉 Cliente aniversariante do mês!",
    "anamnese": "🧾 Ficha de Anamnese",
    "tecnica": "💅 Escolha da Técnica",
    "simulacao": "🎨 Simulação Visual",
    "foto": "Foto original",
    "foto_editada": "Foto com efeito",
    "agendamento": "📅 Agendamento",
    "data": "Data do atendimento",
    "horario": "Horário disponível",
    "observacoes": "📝 Observações Extras",
    "salvar": "Salvar atendimento",
    "sucesso": "Ficha salva com sucesso!",
    "historico": "📊 Histórico de Atendimento"
}

st.title("💻 Sistema Cris Lash")
st.markdown("### Atendimento digital completo com segurança e estilo")

# Sessão de histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# 🗂️ Bloco 1: Cadastro
with st.form("cadastro"):
    st.subheader(txt["cadastro"])
    nome = st.text_input(txt["nome"])
    telefone = st.text_input(txt["telefone"])
    nascimento = st.date_input(txt["nascimento"])
    hoje = datetime.date.today()
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"{txt['idade']}: {idade} anos")
    if nascimento.month == hoje.month:
        st.success(txt["aniversario"])
    if idade < 18:
        responsavel = st.text_input(txt["responsavel"])
        st.warning(txt["alerta_menor"])
    else:
        responsavel = ""
    autorizacao = st.radio(txt["autorizacao"], ["Sim", "Não", "Pendente"])

    enviado_cadastro = st.form_submit_button(txt["salvar"])

# 🧾 Bloco 2: Ficha de Anamnese
with st.expander(txt["anamnese"]):
    lentes = st.radio("Usa lentes de contato?", ["Sim", "Não"])
    alergia = st.radio("Tem histórico de alergias nos olhos ou pálpebras?", ["Sim", "Não"])
    conjuntivite = st.radio("Já teve conjuntivite nos últimos 30 dias?", ["Sim", "Não"])
    irritacao = st.radio("Está com olhos irritados ou lacrimejando frequentemente?", ["Sim", "Não"])
    gravida = st.radio("Está grávida ou amamentando?", ["Sim", "Não"])
    colirio = st.radio("Faz uso de colírios com frequência?", ["Sim", "Não"])
    infeccao = st.radio("Tem blefarite, terçol ou outras infecções oculares?", ["Sim", "Não"])
    cirurgia = st.radio("Fez cirurgia ocular recentemente?", ["Sim", "Não"])
    acido = st.radio("Está em tratamento dermatológico com ácido?", ["Sim", "Não"])
    sensibilidade = st.radio("Tem sensibilidade a produtos químicos ou cosméticos?",
