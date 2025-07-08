# Sistema Cris Lash • Multilíngue (PT/ES/EN) • Streamlit

import streamlit as st
from PIL import Image, ImageEnhance
import datetime

# Dicionário de idiomas
textos = {
    "pt": {
        "boas_vindas": "Bem-vinda ao seu atendimento digital! Preencha seus dados abaixo.",
        "nome": "Nome completo",
        "idade": "Idade",
        "responsavel": "Nome do responsável (se menor)",
        "atendimento": "Tipo de atendimento",
        "autorizacao": "Autorização recebida?",
        "data": "Data do atendimento",
        "observacoes": "Observações extras",
        "alerta_menor": "Cliente menor de idade — exige atenção especial.",
        "tecnica": "Técnica desejada",
        "valor": "Valor estimado",
        "filtro": "Envie uma foto para simular resultado",
        "foto": "Foto original",
        "foto_editada": "Foto com efeito",
        "agenda": "Escolha a data e horário",
        "salvar": "Salvar atendimento",
        "sucesso": "Ficha salva com sucesso!"
    },
    "es": {
        "boas_vindas": "Bienvenida a tu atención digital. Completa tus datos abajo.",
        "nome": "Nombre completo",
        "idade": "Edad",
        "responsavel": "Nombre del responsable (si es menor)",
        "atendimento": "Tipo de atención",
        "autorizacao": "¿Autorización recibida?",
        "data": "Fecha del servicio",
        "observacoes": "Observaciones extras",
        "alerta_menor": "Cliente menor — requiere atención especial.",
        "tecnica": "Técnica deseada",
        "valor": "Valor estimado",
        "filtro": "Sube una foto para simular resultado",
        "foto": "Foto original",
        "foto_editada": "Foto con efecto",
        "agenda": "Elige fecha y hora",
        "salvar": "Guardar atención",
        "sucesso": "¡Ficha guardada con éxito!"
    },
    "en": {
        "boas_vindas": "Welcome to your digital lash service. Fill in your details below.",
        "nome": "Full name",
        "idade": "Age",
        "responsavel": "Guardian’s name (if underage)",
        "atendimento": "Type of appointment",
        "autorizacao": "Authorization received?",
        "data": "Date of service",
        "observacoes": "Extra notes",
        "alerta_menor": "Underage client — special attention required.",
        "tecnica": "Desired technique",
        "valor": "Estimated value",
        "filtro": "Upload a photo to simulate result",
        "foto": "Original photo",
        "foto_editada": "Photo with effect",
        "agenda": "Choose date and time",
        "salvar": "Save intake",
        "sucesso": "Form saved successfully!"
    }
}

# Escolha de idioma
idioma = st.selectbox("Escolha o idioma / Choose language / Elige idioma", ["pt", "es", "en"])
txt = textos[idioma]

st.title("Sistema Cris Lash")
st.markdown(f"### {txt['boas_vindas']}")

# Formulário da cliente
nome = st.text_input(txt["nome"])
idade = st.number_input(txt["idade"], min_value=0)
if idade < 18:
    responsavel = st.text_input(txt["responsavel"])
    st.warning(txt["alerta_menor"])
autorizacao = st.radio(txt["autorizacao"], ["Sim", "Não", "Pendente"])
tipo_atendimento = st.selectbox(txt["atendimento"], ["Normal", "Domingo", "Feriado", "Noturno"])
data_atendimento = st.date_input(txt["data"], value=datetime.date.today())
obs = st.text_area(txt["observacoes"])

st.markdown("---")
st.subheader(txt["tecnica"])

tecnicas = {
    "Fio a Fio": 150,
    "Volume Brasileiro": 180,
    "Volume Russo": 250,
    "Híbrido": 220,
    "Mega Volume": 260,
    "Efeito Delineado": 200
}

tecnica_escolhida = st.selectbox("Escolha a técnica", list(tecnicas.keys()))
st.write(f"{txt['valor']}: R${tecnicas[tecnica_escolhida]}")

st.markdown("---")
st.subheader(txt["filtro"])

foto = st.file_uploader("Upload da imagem", type=["jpg", "jpeg", "png"])
if foto:
    imagem = Image.open(foto)
    st.image(imagem, caption=txt["foto"])
    realce = ImageEnhance.Contrast(imagem).enhance(1.3)
    st.image(realce, caption=txt["foto_editada"])

st.markdown("---")
st.subheader(txt["agenda"])
hora = st.time_input(txt["agenda"])

if st.button(txt["salvar"]):
    st.success(txt["sucesso"])
!streamlit run app.py &>/content/logs.txt &
