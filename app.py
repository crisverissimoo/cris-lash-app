import streamlit as st
from datetime import datetime
import pytz

# 🌍 Fuso horário
fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

# 🎨 Página
st.set_page_config("Consultoria Cris Lash", layout="wide")

# 🔐 Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None
if "ficha_validada" not in st.session_state:
    st.session_state.ficha_validada = False

# 🌐 Idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    idioma = st.selectbox("🌐 Idioma / Idioma", ["Português", "Español"], key="idioma")

    def txt(pt, es):
        return pt if idioma == "Português" else es

    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash', 'Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.write(f"📅 {txt('Hoje é', 'Hoy es')} `{hoje.strftime('%d/%m/%Y')}`")

    # 🗂️ Cadastro
    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente")):
        nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"), key="nome_cliente")
        nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"), min_value=datetime(1920,1,1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"), key="telefone")
        email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"), key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 {txt('Idade:', 'Edad:')} **{idade} {txt('anos', 'años')}**")

        autorizada = True
        if menor:
            responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"), key="responsavel")
            autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"), ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.", "❌ Cliente menor sin autorización — atención bloqueada."))
                autorizada = False

        if nascimento.month == hoje.month and nome:
            st.success(txt(f"🎉 Parabéns, {nome}! Este mês é seu aniversário 💝", f"🎉 Felicidades, {nome}! Este mes es tu cumpleaños 💝"))

    # 🧾 Ficha Clínica
    if autorizada:
        with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Ficha Clínica")):
            with st.form("form_clinica"):
                perguntas = {
                    "lentes": txt("Usa lentes de contato?", "¿Usa lentes de contacto?"),
                    "alergia": txt("Tem histórico de alergias nos olhos ou pálpebras?", "¿Tiene alergias en los ojos o párpados?"),
                    "conjuntivite": txt("Já teve conjuntivite nos últimos 30 dias?", "¿Tuvo conjuntivitis en los últimos 30 días?"),
                    "irritacao": txt("Está com olhos irritados ou lacrimejando frequentemente?", "¿Tiene ojos irritados o llorosos con frecuencia?"),
                    "gravida": txt("Está grávida ou amamentando?", "¿Está embarazada o amamantando?"),
                    "colirio": txt("Faz uso de colírios com frequência?", "¿Usa colirios con frecuencia?"),
                    "infeccao": txt("Tem blefarite, terçol ou outras infecções oculares?", "¿Tiene blefaritis, orzuelos u otras infecciones oculares?"),
                    "cirurgia": txt("Fez cirurgia ocular recentemente?", "¿Ha tenido cirugía ocular reciente?"),
                    "acido": txt("Está em tratamento dermatológico com ácido?", "¿Está en tratamiento dermatológico con ácidos?"),
                    "sensibilidade": txt("Tem sensibilidade a produtos químicos ou cosméticos?", "¿Tiene sensibilidad a productos químicos o cosméticos?"),
                    "extensao": txt("Já fez extensão de cílios antes?", "¿Ya se ha hecho extensiones de pestañas antes?"),
                    "reacao": txt("Teve alguma reação alérgica em procedimentos anteriores?", "¿Tuvo alguna reacción alérgica en procedimientos anteriores?"),
                    "glaucoma": txt("Possui glaucoma ou outra condição ocular diagnosticada?", "¿Tiene glaucoma u otra condición ocular diagnosticada?")
                }

                respostas = {}
                for chave, pergunta in perguntas.items():
                    respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

                enviar = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar formulario"))

                if enviar:
                    if "Sim" in respostas.values():
                        st.error(txt("⚠️ Cliente não está apta — atendimento bloqueado.", "⚠️ Cliente no apta — atención bloqueada."))
                        st.session_state.ficha_validada = False
                    else:
                        st.success(txt("✅ Ficha clínica validada com sucesso.", "✅ Ficha validada correctamente."))
                        st.session_state.ficha_validada = True

    # Etapas seguintes — só se apta
    if st.session_state.ficha_validada:
        with st.expander(txt("🎨 Escolha da Técnica", "🎨 Elige la técnica")):
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
            data = st.date_input(txt("Data do atendimento", "Fecha de la cita"), key="data_atendimento")
            hora = st.time_input(txt("Horário do atendimento", "Hora de la cita"), key="horario_atendimento")

        with st.expander(txt("📝 Observações", "📝 Observaciones")):
            observacoes = st.text_area(txt("Notas do
