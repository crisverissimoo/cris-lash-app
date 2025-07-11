import streamlit as st
from PIL import Image
from datetime import datetime
import pytz

# 🌍 Fuso horário local
fuso_espanha = pytz.timezone("Europe/Madrid")
agora_local = datetime.now(fuso_espanha)
hoje = agora_local.date()

# 🎨 Configuração da página
st.set_page_config(page_title="Consultoria Cris Lash", layout="wide")

# 🔐 Estado da sessão
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
    with st.expander("🗂️ Cadastro da Cliente"):
        nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
        nascimento = st.date_input("📅 Data de nascimento", min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input("📞 Telefone", key="telefone")
        email = st.text_input("📧 Email (opcional)", key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 Idade: **{idade} anos**")

        if menor:
            responsavel = st.text_input("👨‍👩‍👧 Nome do responsável", key="responsavel")
            autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error("❌ Cliente menor sem autorização — atendimento bloqueado.")
            autorizada = autorizacao == "Sim"
        else:
            autorizada = True

        if nascimento.month == hoje.month and nome_cliente:
            st.success(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza e carinho! 💝")

  # 🧾 Ficha Clínica
    if autorizada:
    # 🧾 Ficha Clínica
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
                st.success("📋 Ficha clínica registrada com sucesso!")

    # 🎨 Escolha da Técnica
    with st.expander("🎨 Escolha da Técnica"):
        st.write("Selecione a técnica desejada para este atendimento:")
        formatos = {
            "Fio a fio": "✨ Natural, delicado e clássico",
            "Volume russo": "💥 Impactante, curvado e volumoso",
            "Híbrido": "⚖️ Equilíbrio entre clássico e volume",
            "Colorido": "🌈 Criativo e com tons vibrantes"
        }
        for nome, descricao in formatos.items():
            if st.button(nome, key=f"formato_{nome}"):
                st.session_state.formato_escolhido = nome
                st.success(f"Técnica selecionada: **{nome}** — {descricao}")

    # ✨ Estilos Visuais + Indicação
    with st.expander("✨ Estilos Visuais + Indicação"):
        col1, col2 = st.columns(2)

        with col1:
            st.image("static/imgs/classico.png", caption="Clássico", use_container_width=True)
            st.markdown("🔘 **Clássico** — Indicado para todos os tipos de olhos.")

            st.image("static/imgs/boneca.png", caption="Boneca", use_container_width=True)
            st.markdown("🔘 **Boneca** — Olhos pequenos, amendoados ou asiáticos.")

        with col2:
            st.image("static/imgs/gatinho.png", caption="Gatinho", use_container_width=True)
            st.markdown("🔘 **Gatinho** — Olhos juntos, saltados ou amendoados.")

            st.image("static/imgs/esquilo.png", caption="Esquilo", use_container_width=True)
            st.markdown("🔘 **Esquilo** — Olhos caídos, encapotados ou amendoados.")

    # 📅 Agendamento
    with st.expander("📅 Agendamento"):
        st.date_input("Data do atendimento", key="data_atendimento")
        st.time_input("Horário do atendimento", key="horario_atendimento")

    # 📝 Observações
    with st.expander("📝 Observações Personalizadas"):
        st.text_area("Anotações do atendimento", key="observacoes_cliente")

    # 📚 Histórico
    with st.expander("📚 Histórico da Cliente"):
        st.text_area("Últimos atendimentos ou observações relevantes", key="historico_cliente")

    # 🧾 Registro da Sessão
    registro = {
        "Tipo de olho": st.session_state.get("tipo_olho", ""),
        "Técnica sugerida": st.session_state.get("sugestao_tecnica", ""),
        "Técnica escolhida": st.session_state.get("formato_escolhido", ""),
        "Data": st.session_state.get("data_atendimento", ""),
        "Horário": st.session_state.get("horario_atendimento", ""),
        "Histórico": st.session_state.get("historico_cliente", ""),
        "Observações": st.session_state.get("observacoes_cliente", "")
    }

    if "historico" not in st.session_state:
        st.session_state.historico = []

    st.session_state.historico.append(registro)
    st.success("✅ Atendimento registrado com sucesso!")

    # 📋 Exibir registros salvos
    if st.session_state.historico:
        for i, atend in enumerate(st.session_state.historico[::-1]):
            st.markdown(f"### 🧍 Atendimento #{len(st.session_state.historico)-i}")
            st.write(f"📅 Data: `{atend['Data']} — {atend['Horário']}`")
            st.write(f"👁️ Tipo de olho: **{atend['Tipo de olho']}**")
            st.write(f"💡 Sugestão de técnica: *{atend['Técnica sugerida']}*")
            st.write(f"🎨 Técnica escolhida: **{atend['Técnica escolhida']}**")
            if atend["Observações"]:
                st.markdown(f"📝 Observações: {atend['Observações']}")
            st.markdown("---")
    else:
        st.info("ℹ️ Nenhum atendimento registrado ainda.")
else:
    st.warning("⚠️ Atendimento bloqueado — cliente menor sem autorização válida.")

