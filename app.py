import streamlit as st
from datetime import datetime
import pytz

# 🌍 Fuso horário
fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

# 🎨 Configuração de página
st.set_page_config("Consultoria Cris Lash", layout="wide")

# 🔐 Estado de sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None
if "ficha_validada" not in st.session_state:
    st.session_state.ficha_validada = False

# 🌐 Escolha de idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    idioma = st.selectbox("🌐 Escolha o idioma / Elige el idioma", ["Português", "Español"], key="idioma")

    def txt(pt, es):
        return pt if idioma == "Português" else es

    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash', 'Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.write(f"📅 {txt('Hoje é', 'Hoy es')} `{hoje.strftime('%d/%m/%Y')}`")

    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente")):
        nome_cliente = st.text_input("🧍 " + txt("Nome completo", "Nombre completo"), key="nome_cliente")
        nascimento = st.date_input("📅 " + txt("Data de nascimento", "Fecha de nacimiento"), min_value=datetime(1920,1,1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input("📞 " + txt("Telefone", "Teléfono"), key="telefone")
        email = st.text_input("📧 Email (opcional)", key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 {txt('Idade:', 'Edad:')} **{idade} {txt('anos', 'años')}**")

        autorizada = True
        if menor:
            responsavel = st.text_input("👨‍👩‍👧 " + txt("Nome do responsável", "Nombre del responsable"), key="responsavel")
            autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"), ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.", "❌ Cliente menor sin autorización — atención bloqueada."))
                autorizada = False

        if nascimento.month == hoje.month and nome_cliente:
            st.success(txt(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário 💝", f"🎉 Felicidades, {nome_cliente}! Este mes es tu cumpleaños 💝"))

    # 🧾 Ficha Clínica
    if autorizada:
        with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Ficha Clínica")):
            with st.form("ficha_anamnese"):
                perguntas = {
                    "lentes": txt("Usa lentes de contato?", "¿Usas lentes de contacto?"),
                    "alergia": txt("Tem alergias nos olhos ou pálpebras?", "¿Tienes alergias en los ojos o párpados?"),
                    "conjuntivite": txt("Teve conjuntivite nos últimos 30 dias?", "¿Tuviste conjuntivitis en los últimos 30 días?"),
                    "gravida": txt("Está grávida ou amamentando?", "¿Estás embarazada o amamantando?"),
                    "colirio": txt("Usa colírios com frequência?", "¿Usas colirios con frecuencia?"),
                    "cirurgia": txt("Fez cirurgia ocular recente?", "¿Has tenido cirugía ocular reciente?"),
                    "reacao": txt("Teve reação alérgica com cílios antes?", "¿Tuviste reacción alérgica con extensiones antes?")
                }

                respostas = {}
                for chave, pergunta in perguntas.items():
                    respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

                enviar_ficha = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar ficha"))

                if enviar_ficha:
                    if "Sim" in respostas.values():
                        st.error(txt("⚠️ Cliente não está apta — atendimento bloqueado.", "⚠️ Cliente no apta — atención bloqueada."))
                        st.session_state.ficha_validada = False
                    else:
                        st.success(txt("✅ Ficha validada com sucesso.", "✅ Ficha validada correctamente."))
                        st.session_state.ficha_validada = True

    # 👁️ Próximas etapas — só se apta
    if st.session_state.ficha_validada:
        with st.expander(txt("🎨 Escolha da Técnica", "🎨 Elige la Técnica")):
            st.write(txt("Selecione a técnica desejada:", "Selecciona la técnica deseada:"))
            tecnicas = {
                "Fio a fio": txt("✨ Natural, delicado e clássico", "✨ Natural, delicado y clásico"),
                "Volume russo": txt("💥 Impactante, curvado e volumoso", "💥 Impactante, curvado y voluminoso"),
                "Híbrido": txt("⚖️ Equilíbrio entre clássico e volume", "⚖️ Equilibrio entre clásico y volumen"),
                "Colorido": txt("🌈 Criativo e com cor", "🌈 Creativo y con color")
            }
            for nome, descricao in tecnicas.items():
                if st.button(nome, key=f"formato_{nome}"):
                    st.session_state.formato_escolhido = nome
                    st.success(f"{txt('Técnica escolhida:', 'Técnica elegida:')} **{nome}** — {descricao}")

        with st.expander(txt("✨ Estilos Visuais + Indicação", "✨ Estilos Visuales + Indicaciones")):
            colA, colB = st.columns(2)
            with colA:
                st.image("static/imgs/classico.png", caption="Clássico", use_container_width=True)
                st.markdown("🔘 **Clássico** — " + txt("Todos os tipos de olhos.", "Todos los tipos de ojos."))
                st.image("static/imgs/boneca.png", caption="Boneca", use_container_width=True)
                st.markdown("🔘 **Boneca** — " + txt("Pequenos, amendoados ou asiáticos.", "Pequeños, almendrados o asiáticos."))
            with colB:
                st.image("static/imgs/gatinho.png", caption="Gatinho", use_container_width=True)
                st.markdown("🔘 **Gatinho** — " + txt("Juntos ou saltados.", "Juntos o saltones."))
                st.image("static/imgs/esquilo.png", caption="Esquilo", use_container_width=True)
                st.markdown("🔘 **Esquilo** — " + txt("Caídos ou encapotados.", "Caídos o encapotados."))

        with st.expander(txt("📅 Agendamento", "📅 Cita")):
            st.date_input(txt("Data do atendimento", "Fecha de la cita"), key="data_atendimento")
            st.time_input(txt("Horário do atendimento", "Hora de la cita"), key="horario_atendimento")

        with st.expander(txt("📝 Observações", "📝 Observaciones")):
            st.text_area(txt("Notas do atendimento", "Notas de la sesión"), key="observacoes_cliente")

        with st.expander(txt("📚 Histórico", "📚 Historial")):
            st.text_area(txt("Observações anteriores", "Observaciones anteriores"), key="historico_cliente")

        registro = {
            "Nome": nome_cliente,
            "Técnica": st.session_state.formato_escolhido,
            "Data": st.session_state.get("data_atendimento", ""),
            "Horário": st.session_state.get("horario_atendimento", ""),
            "Histórico": st.session_state.get("historico_cliente", ""),
            "Observações": st.session_state.get("observacoes_cliente", "")
        }

        st.session_state.historico.append(registro)
        st.success(txt("✅ Atendimento registrado!", "✅ Atención registrada!"))

        if st.session_state.historico:
    for i, atend in enumerate(st.session_state.historico[::-1]):
        st.markdown(f"### 🧍 Atendimento #{len(st.session_state.historico) - i}")
        st.write(f"📅 Data: `{atend['Data']} — {atend['Horário']}`")
        st.write(f"👁️ Tipo de olho: **{atend.get('Tipo de olho', 'N/A')}**")
        st.write(f"💡 Sugestão de técnica: *{atend.get('Técnica sugerida', 'N/A')}*")
        st.write(f"🎨 Técnica escolhida: **{atend.get('Técnica escolhida', 'N/A')}**")
        if atend.get("Observações"):
            st.markdown(f"📝 Observações: {atend['Observações']}")
        st.markdown("---")
else:
    st.info("ℹ️ Nenhum atendimento registrado ainda.")

