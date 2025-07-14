import streamlit as st
from datetime import datetime, date, timedelta
import pytz

fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()
st.set_page_config("Consultoria Cris Lash", layout="wide")

def txt(pt, es): return pt if st.session_state.get("idioma", "Português") == "Português" else es

# Estados iniciais
for key in ["ficha_validada", "cliente_apta", "efeito_escolhido", "tipo_aplicacao", "valor", "agendamento_confirmado"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "historico_ocupados" not in st.session_state:
    st.session_state.historico_ocupados = []

# 🎀 Boas-vindas + idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.selectbox("🌐 Idioma / Language", ["Português", "Español"], key="idioma")
    st.markdown("""
    <div style='background-color:#fff2f2; padding:15px; border-radius:10px; border-left:5px solid #e09b8e; color:#333'>
    👋 <strong>Bem-vinda ao Cris Lash!</strong><br>
    ✨ Atendimento profissional com técnica em formação.<br>
    💶 Valor promocional de lançamento: <strong>10€</strong> por aplicação!
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash','Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.write(f"📅 {txt('Hoje é','Hoy es')} `{hoje.strftime('%d/%m/%Y')}`")

# 👤 Ficha da cliente
with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente")):
    nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"), key="nome_cliente")
    nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                               min_value=date(1920, 1, 1), max_value=hoje, key="nascimento")
    telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"), key="telefone")
    email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"), key="email")
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"📌 {txt('Idade:','Edad:')} **{idade} {txt('anos','años')}**")

    autorizada = True
    if idade < 18:
        responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"))
        autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"), ["Sim", "Não", "Pendente"])
        if autorizacao != "Sim":
            st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.", "❌ Cliente menor sin autorización — atención bloqueada."))
            autorizada = False

# 🧾 Ficha clínica
if autorizada:
    respostas = {}
    col_e, col_c, col_d = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<h4 style='text-align:center;'>🧾 " + txt("Ficha de Anamnese Clínica", "Ficha Clínica") + "</h4>", unsafe_allow_html=True)
        with st.form("form_clinica"):
            perguntas = {
                "glaucoma": txt("Possui glaucoma?", "¿Tiene glaucoma?"),
                "infeccao": txt("Tem infecções oculares?", "¿Tiene infecciones oculares?"),
                "conjuntivite": txt("Conjuntivite recente?", "¿Conjuntivitis reciente?"),
                "cirurgia": txt("Cirurgia ocular recente?", "¿Cirugía ocular reciente?"),
                "reacao": txt("Reação alérgica anterior?", "¿Reacción alérgica previa?"),
                "alergia": txt("Histórico de alergias?", "¿Historial de alergias?"),
                "gravida": txt("Está grávida ou amamentando?", "¿Está embarazada o lactante?"),
                "acido": txt("Tratamento com ácido?", "¿Tratamiento con ácidos?"),
                "irritacao": txt("Olhos irritados?", "¿Ojos irritados?"),
                "sensibilidade": txt("Sensibilidade a químicos?", "¿Sensibilidad a químicos?"),
                "colirio": txt("Uso frequente de colírios?", "¿Uso frecuente de colirios?"),
                "lentes": txt("Usa lentes de contato?", "¿Usa lentes de contacto?"),
                "extensao": txt("Já fez extensão antes?", "¿Ya se hizo extensiones?")
            }
            for chave, pergunta in perguntas.items():
                respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")
            enviar = st.form_submit_button("📨 " + txt("Finalizar ficha", "Finalizar formulario"))

        if enviar:
            if any(r is None for r in respostas.values()):
                st.warning(txt("⚠️ Responda todas as perguntas.", "⚠️ Responda todas las preguntas."))
            else:
                impeditivos = {"glaucoma", "infeccao", "conjuntivite", "cirurgia", "reacao"}
                alertas = {"alergia", "gravida", "acido", "sensibilidade", "irritacao"}
                infos = {"colirio", "lentes", "extensao"}
                bloc, avis, inf = [], [], []

                for chave, resposta in respostas.items():
                    if resposta == "Sim":
                        if chave in impeditivos: bloc.append(f"- {perguntas[chave]}")
                        elif chave in alertas: avis.append(f"- {perguntas[chave]}")
                        elif chave in infos: inf.append(f"- {perguntas[chave]}")

                if bloc:
                    st.error("❌ " + txt("Cliente não está apta para atendimento.", "Cliente no apta para atención") + "\n\n" + "\n".join(bloc))
                    st.session_state.ficha_validada = False
                    st.session_state.cliente_apta = False
                    st.stop()
                else:
                    if avis: st.warning("⚠️ " + txt("Condições que requerem avaliação:", "Condiciones que requieren evaluación:") + "\n\n" + "\n".join(avis))
                    if inf: st.info("📎 " + txt("Informações adicionais:", "Información adicional:") + "\n\n" + "\n".join(inf))
                    st.success("✅ " + txt("Cliente apta — ficha validada!", "Cliente apta — ficha validada!"))
                    st.session_state.ficha_validada = True
                    st.session_state.cliente_apta = True

# 🔓 Etapas seguintes — liberadas após ficha validada
if st.session_state.get("ficha_validada") and st.session_state.get("cliente_apta"):

    # ✨ Escolha de Efeito
    st.markdown("<h4 style='text-align:center;'>✨ Escolha o Efeito Lash</h4>", unsafe_allow_html=True)
    efeitos = {
        "Clássica": {
            "img": "https://i.imgur.com/Nqrwdcm.png",
            "desc": txt("Fios distribuídos uniformemente — efeito natural e delicado", "Fibras distribuidas uniformemente — efecto natural y delicado"),
            "tipo_olho": txt("Olhos amendoado ou simétricos", "Ojos almendrados o simétricos")
        },
        "Boneca": {
            "img": "https://i.imgur.com/vJUuvsl.png",
            "desc": txt("Maior concentração no centro — arredonda o olhar", "Mayor concentración en el centro — redondea la mirada"),
            "tipo_olho": txt("Olhos pequenos, fechados ou orientais", "Ojos pequeños, cerrados u orientales")
        },
        "Gatinho": {
            "img": "https://i.imgur.com/zpBFK0e.png",
            "desc": txt("Fios longos no canto externo — efeito sensual", "Fibras largas en la esquina externa — efecto sensual"),
            "tipo_olho": txt("Olhos caídos ou arredondados", "Ojos caídos o redondeados")
