import streamlit as st
from PIL import Image, ImageEnhance
import datetime

# Textos em português
txt = {
    "boas_vindas": "Bem-vinda ao seu atendimento digital!",
    "nome": "Nome completo",
    "telefone": "Telefone",
    "idade": "Idade",
    "responsavel": "Nome do responsável (se menor)",
    "alerta_menor": "Cliente menor de idade — exige atenção especial.",
    "autorizacao": "Autorização recebida?",
    "atendimento": "Tipo de atendimento",
    "data": "Data do atendimento",
    "horario": "Horário disponível",
    "tecnica": "Técnica desejada",
    "valor": "Valor estimado",
    "observacoes": "Observações extras",
    "filtro": "Envie uma foto para simular resultado",
    "foto": "Foto original",
    "foto_editada": "Foto com efeito",
    "salvar": "Salvar atendimento",
    "sucesso": "Ficha salva com sucesso!"
}

st.title("💻 Sistema Cris Lash")
st.markdown(f"### {txt['boas_vindas']}")

# 🧾 Ficha da cliente com formulário real
with st.form("ficha_cliente"):
    st.subheader("🧾 Ficha de Atendimento")

    nome = st.text_input(txt["nome"])
    telefone = st.text_input(txt["telefone"])
    idade = st.number_input(txt["idade"], min_value=0)

    if idade < 18:
        responsavel = st.text_input(txt["responsavel"])
        st.warning(txt["alerta_menor"])
    else:
        responsavel = ""

    autorizacao = st.radio(txt["autorizacao"], ["Sim", "Não", "Pendente"])
    tipo_atendimento = st.selectbox(txt["atendimento"], ["Normal", "Domingo", "Feriado", "Noturno"])
    data_atendimento = st.date_input(txt["data"], value=datetime.date.today())

    horarios_disponiveis = [
        "08:00", "08:30", "09:00", "09:30",
        "10:00", "10:30", "11:00", "11:30",
        "14:00", "14:30", "15:00", "15:30",
        "16:00", "16:30", "17:00", "17:30",
        "18:00", "18:30", "19:00"
    ]
    horario_escolhido = st.selectbox(txt["horario"], horarios_disponiveis)

    tecnica_opcoes = {
        "Fio a Fio": 150,
        "Volume Brasileiro": 180,
        "Volume Russo": 250,
        "Híbrido": 220,
        "Mega Volume": 260,
        "Efeito Delineado": 200
    }
    tecnica_escolhida = st.selectbox(txt["tecnica"], list(tecnica_opcoes.keys()))
    valor_formatado = f"€{tecnica_opcoes[tecnica_escolhida]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.write(f"{txt['valor']}: {valor_formatado}")

    obs = st.text_area(txt["observacoes"])

    foto = st.file_uploader(txt["filtro"], type=["jpg", "jpeg", "png"])
    if foto:
        imagem = Image.open(foto)
        st.image(imagem, caption=txt["foto"])
        realce = ImageEnhance.Contrast(imagem).enhance(1.5)
        st.image(realce, caption=txt["foto_editada"])

    enviado = st.form_submit_button(txt["salvar"])
    if enviado:
        st.success(txt["sucesso"])
