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
    st.write(f"📅 Hoje é `{hoje.strftime('%d/%m/%Y')}`")

    # 🗂️ Cadastro
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
                for i, r in enumerate(st.session_state.historico[::-1]):
                    st.markdown(f"---")
                    st.markdown(f"### Atendimento {len(st.session_state.historico)-i}")
                    st.markdown(f"**Cliente:** {r['nome']}")
                    st.markdown(f"**Telefone:** {r['telefone']}")
                    st.markdown(f"**Idade:** {r['idade']} anos")
                    st.markdown(f"**Técnica indicada:** {r['formato']}")
                    st.markdown(f"**Agendado para:** {r['data_agendamento']} às {r['horario']}")
                    st.markdown(f"**Observações:** {r['observacoes']}")
