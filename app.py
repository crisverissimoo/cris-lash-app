import streamlit as st
from datetime import datetime
import pytz

fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

st.set_page_config("Consultoria Cris Lash", layout="wide")

if "historico" not in st.session_state:
    st.session_state.historico = []
if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None
if "ficha_validada" not in st.session_state:
    st.session_state.ficha_validada = False

# 🌐 Idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    idioma = st.selectbox("🌐 Idioma / Language", ["Português", "Español"], key="idioma")
    def txt(pt, es): return pt if idioma == "Português" else es

    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash','Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.write(f"📅 {txt('Hoje é','Hoy es')} `{hoje.strftime('%d/%m/%Y')}`")

    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente")):
        nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"), key="nome_cliente")
        nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"), min_value=datetime(1920,1,1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"), key="telefone")
        email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"), key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 {txt('Idade:','Edad:')} **{idade} {txt('anos','años')}**")

        autorizada = True
        if menor:
            responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"), key="responsavel")
            autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"), ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.", "❌ Cliente menor sin autorización — atención bloqueada."))
                autorizada = False

    # 🧾 Ficha Clínica
    if autorizada:
        with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Ficha Clínica")):
            with st.form("form_clinica"):
                perguntas = {
                    "glaucoma": txt("Possui glaucoma ou outra condição ocular diagnosticada?", "¿Tiene glaucoma u otra condición ocular diagnosticada?"),
                    "infeccao": txt("Tem blefarite, terçol ou outras infecções oculares?", "¿Tiene blefaritis, orzuelos u otras infecciones oculares?"),
                    "conjuntivite": txt("Já teve conjuntivite nos últimos 30 dias?", "¿Tuvo conjuntivitis en los últimos 30 días?"),
                    "cirurgia": txt("Fez cirurgia ocular recentemente?", "¿Ha tenido cirugía ocular reciente?"),
                    "alergia": txt("Tem histórico de alergias nos olhos ou pálpebras?", "¿Tiene alergias en los ojos o párpados?"),
                    "irritacao": txt("Está com olhos irritados ou lacrimejando frequentemente?", "¿Tiene ojos irritados o llorosos frecuentemente?"),
                    "gravida": txt("Está grávida ou amamentando?", "¿Está embarazada o amamantando?"),
                    "acido": txt("Está em tratamento dermatológico com ácido?", "¿Está en tratamiento con ácidos dermatológicos?"),
                    "sensibilidade": txt("Tem sensibilidade a produtos químicos ou cosméticos?", "¿Tiene sensibilidad a productos químicos o cosméticos?"),
                    "colirio": txt("Faz uso de colírios com frequência?", "¿Usa colirios con frecuencia?"),
                    "lentes": txt("Usa lentes de contato?", "¿Usa lentes de contacto?"),
                    "extensao": txt("Já fez extensão de cílios antes?", "¿Ya se hizo extensiones de pestañas?"),
                    "reacao": txt("Teve alguma reação alérgica em procedimentos anteriores?", "¿Tuvo alguna reacción alérgica en procedimientos anteriores?")
                }

                respostas = {}
                for chave, pergunta in perguntas.items():
                    respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

                enviar = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar formulario"))


if enviar:
    # ❌ Motivos impeditivos
    impeditivos = {
        "glaucoma": "Glaucoma ou condição ocular diagnosticada",
        "infeccao": "Infecção ocular (blefarite, terçol, etc)",
        "conjuntivite": "Conjuntivite recente (últimos 30 dias)",
        "cirurgia": "Cirurgia ocular recente",
        "reacao": "Reação alérgica em procedimentos anteriores"
    }

    # ⚠️ Motivos de alerta
    alerta = {
        "alergia": "Histórico de alergias nos olhos ou pálpebras",
        "irritacao": "Olhos irritados ou lacrimejando frequentemente",
        "gravida": "Gestante ou lactante — recomenda-se autorização médica",
        "acido": "Tratamento dermatológico com ácido",
        "sensibilidade": "Sensibilidade a produtos químicos ou cosméticos"
    }

    # ✅ Informativos
    informativos = {
        "colirio": "Uso de colírios frequente",
        "lentes": "Usa lentes de contato",
        "extensao": "Já fez extensão de cílios antes"
    }

    bloqueios_detectados = []
    alertas_detectados = []
    info_detectados = []

    for chave, resposta in respostas.items():
        if resposta == "Sim":
            if chave in impeditivos:
                bloqueios_detectados.append(f"❌ {impeditivos[chave]}")
            elif chave in alerta:
                alertas_detectados.append(f"⚠️ {alerta[chave]}")
            elif chave in informativos:
                info_detectados.append(f"📌 {informativos[chave]}")

    if bloqueios_detectados:
    st.error("❌ Cliente **não está apta para atendimento**.\n\n" +
             "\n".join([f"- {motivo}" for motivo in bloqueios_detectados]))
    st.session_state.ficha_validada = False

else:
    if alertas_detectados:
        st.warning("⚠️ **Atenção!** Condições que requerem avaliação profissional:\n\n" +
                   "\n".join([f"- {motivo}" for motivo in alertas_detectados]))

    if info_detectados:
        st.info("📎 Informações adicionais para registro:\n\n" +
                "\n".join([f"- {motivo}" for motivo in info_detectados]))

    st.success("✅ Cliente **apta para continuar** — ficha clínica validada com sucesso.")
    st.session_state.ficha_validada = True



