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
if "cliente_apta" in st.session_state and st.session_state.cliente_apta == False:
    st.error("❌ Cliente não está apta para atendimento. Reação alérgica ou condição contraindicada.")
    st.stop()

# 🌐 Idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    idioma = st.selectbox("🌐 Idioma / Language", ["Português", "Español"], key="idioma")
    def txt(pt, es): return pt if idioma == "Português" else es

    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash','Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.write(f"📅 {txt('Hoje é','Hoy es')} `{hoje.strftime('%d/%m/%Y')}`")

    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente")):
        st.markdown("<h4 style='text-align:center;'>🗂️ Cadastro da Cliente</h4>", unsafe_allow_html=True)

        nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"), key="nome_cliente")
        nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                                   min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"), key="telefone")
        email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"), key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 {txt('Idade:','Edad:')} **{idade} {txt('anos','años')}**")

        autorizada = True
        if menor:
            responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"), key="responsavel")
            autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"),
                                   ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.",
                             "❌ Cliente menor sin autorización — atención bloqueada."))
                autorizada = False

if autorizada:
    respostas = {}

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("<h4 style='text-align:center;'>🧾 Ficha de Anamnese Clínica</h4>", unsafe_allow_html=True)

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

            for chave, pergunta in perguntas.items():
                col_p = st.columns([1, 4, 1])[1]
                with col_p:
                    respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

            col_btn = st.columns([1, 2, 1])[1]
            with col_btn:
                enviar = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar formulario"))

            if enviar:
                if any(resposta is None for resposta in respostas.values()):
                    st.warning("⚠️ " + txt("Você precisa responder todas as perguntas antes de finalizar.",
                                            "Debe responder todas las preguntas antes de continuar."))
                    st.session_state.ficha_validada = False
                else:
                    impeditivos = {
                        "glaucoma": txt("Glaucoma ou condição ocular diagnosticada", "Glaucoma u otra condición ocular"),
                        "infeccao": txt("Infecção ocular", "Infección ocular"),
                        "conjuntivite": txt("Conjuntivite recente", "Conjuntivitis reciente"),
                        "cirurgia": txt("Cirurgia ocular recente", "Cirugía ocular reciente"),
                        "reacao": txt("Reação alérgica anterior", "Reacción alérgica anterior")
                    }
                    alerta = {
                        "alergia": txt("Histórico de alergias", "Historial de alergias"),
                        "irritacao": txt("Olhos irritados", "Ojos irritados"),
                        "gravida": txt("Gestante ou lactante", "Embarazada o lactante"),
                        "acido": txt("Tratamento com ácido", "Tratamiento con ácido"),
                        "sensibilidade": txt("Sensibilidade a químicos", "Sensibilidad química")
                    }
                    informativos = {
                        "colirio": txt("Uso frequente de colírios", "Uso frecuente de colirios"),
                        "lentes": txt("Usa lentes de contato", "Usa lentes de contacto"),
                        "extensao": txt("Já fez extensão antes", "Ya se hizo extensiones")
                    }

                    bloqueios_detectados = []
                    alertas_detectados = []
                    info_detectados = []

                    for chave, resposta in respostas.items():
                        if resposta == "Sim":
                            if chave in impeditivos:
                                bloqueios_detectados.append(f"- {impeditivos[chave]}")
                            elif chave in alerta:
                                alertas_detectados.append(f"- {alerta[chave]}")
                            elif chave in informativos:
                                info_detectados.append(f"- {informativos[chave]}")

                    if bloqueios_detectados:
                        st.error("❌ " + txt("Cliente não está apta para atendimento.",
                                            "Cliente no apta para atención") + "\n\n" +
                                 "\n".join(bloqueios_detectados))
                        st.session_state.ficha_validada = False
                        st.session_state.cliente_apta = False
                        st.stop()
                    else:
                        if alertas_detectados:
                            st.warning("⚠️ " + txt("Condições que requerem avaliação profissional:",
                                                   "Condiciones que requieren evaluación profesional:") + "\n\n" +
                                       "\n".join(alertas_detectados))
                        if info_detectados:
                            st.info("📎 " + txt("Informações adicionais para registro:",
                                               "Información adicional para el registro:") + "\n\n" +
                                    "\n".join(info_detectados))
                        st.success("✅ " + txt("Cliente apta para continuar — ficha validada com sucesso.",
                                               "Cliente apta para continuar — ficha validada correctamente."))
                        st.session_state.ficha_validada = True
                        st.session_state.cliente_apta = True

# 🔓 Etapa 2 — Escolha de Efeito
 
if st.session_state.ficha_validada:
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("<h4 style='text-align:center;'>✨ Escolha o Efeito Lash</h4>", unsafe_allow_html=True)

        efeitos = {
            "Clássica": {
                "img": "https://i.imgur.com/Nqrwdcm.png",
                "desc": txt("Fios distribuídos uniformemente — efeito natural e delicado", "Fibras distribuidas uniformemente — efecto natural y delicado"),
                "tipo_olho": txt("Olhos amendoado ou simétricos", "Ojos almendrados o simétricos")
            },
            "Boneca": {
                "img": "https://i.imgur.com/vJUuvsl.png",
                "desc": txt("Maior concentração no centro — abre e arredonda o olhar", "Mayor concentración en el centro — abre y redondea la mirada"),
                "tipo_olho": txt("Olhos pequenos, fechados ou orientais", "Ojos pequeños, cerrados u orientales")
            },
            "Gatinho": {
                "img": "https://i.imgur.com/zpBFK0e.png",
                "desc": txt("Fios longos no canto externo — efeito sensual e alongado", "Fibras largas en la esquina externa — efecto sensual y alargado"),
                "tipo_olho": txt("Olhos caídos ou arredondados", "Ojos caídos o redondeados")
            },
            "Esquilo": {
                "img": "https://i.imgur.com/BY5eEsr.png",
                "desc": txt("Volume acentuado entre o centro e canto externo — estilo marcante", "Volumen acentuado entre el centro y la esquina externa — estilo llamativo"),
                "tipo_olho": txt("Olhos puxados ou olhos grandes", "Ojos rasgados o grandes")
            }
        }

        for nome, efeito in efeitos.items():
            st.markdown("""
                <div style='
                    border: 2px solid #e09b8e;
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 30px;
                '>
            """, unsafe_allow_html=True)

            col_img, col_txt = st.columns([1.6, 1.4])

            with col_img:
                st.markdown("""
                    <div style='
                        display: flex;
                        justify-content: center;
                        padding-top: 120px;
                    '>
                """, unsafe_allow_html=True)
                st.image(efeito["img"], width=460)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_txt:
                st.markdown(f"""
                    <h5 style='
                        margin-top:0;
                        text-align:center;
                    '>{txt(f"Efeito {nome}", f"Efecto {nome}")}</h5>
                """, unsafe_allow_html=True)
                st.write(efeito["desc"])
                st.markdown("👁️ " + txt("Indicado para:", "Indicado para:") + f" **{efeito['tipo_olho']}**")

                col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
                with col_b2:
                    if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"btn_{nome}"):
                        st.session_state.efeito_escolhido = nome

            st.markdown("</div>", unsafe_allow_html=True)

        if "efeito_escolhido" in st.session_state:
            nome = st.session_state.efeito_escolhido
            st.success("✅ " + txt(
                f"Efeito selecionado: {nome}\n{efeitos[nome]['desc']}",
                f"Efecto seleccionado: {nome}\n{efeitos[nome]['desc']}"
            ))


