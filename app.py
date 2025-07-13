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
    with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Ficha Clínica")):
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

                respostas = {}
            for chave, pergunta in perguntas.items():
                col_b = st.columns([1, 4, 1])[1]
                with col_b:
                    respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

            col_botao = st.columns([1, 2, 1])[1]
            with col_botao:
                enviar = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar formulario"))

        if enviar:
                    impeditivos = {
                        "glaucoma": txt("Glaucoma ou condição ocular diagnosticada", "Glaucoma u otra condición ocular"),
                        "infeccao": txt("Infecção ocular (blefarite, terçol, etc)", "Infección ocular (blefaritis, orzuelos, etc)"),
                        "conjuntivite": txt("Conjuntivite recente (últimos 30 dias)", "Conjuntivitis reciente (últimos 30 días)"),
                        "cirurgia": txt("Cirurgia ocular recente", "Cirugía ocular reciente"),
                        "reacao": txt("Reação alérgica em procedimentos anteriores", "Reacción alérgica en procedimientos anteriores")
                    }

                    alerta = {
                        "alergia": txt("Histórico de alergias nos olhos ou pálpebras", "Historial de alergias en ojos o párpados"),
                        "irritacao": txt("Olhos irritados ou lacrimejando frequentemente", "Ojos irritados o llorosos frecuentemente"),
                        "gravida": txt("Gestante ou lactante — recomenda-se autorização médica", "Embarazada o lactante — se recomienda autorización médica"),
                        "acido": txt("Tratamento dermatológico com ácido", "Tratamiento dermatológico con ácido"),
                        "sensibilidade": txt("Sensibilidade a produtos químicos ou cosméticos", "Sensibilidad a productos químicos o cosméticos")
                    }

                    informativos = {
                        "colirio": txt("Uso de colírios frequente", "Uso frecuente de colirios"),
                        "lentes": txt("Usa lentes de contato", "Usa lentes de contacto"),
                        "extensao": txt("Já fez extensão de cílios antes", "Ya se hizo extensiones de pestañas")
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
                        st.error("❌ " + txt("Cliente **não está apta para atendimento**.", "Cliente no apta para atención") + "\n\n" +
                                 "\n".join(bloqueios_detectados))
                        st.session_state.ficha_validada = False
                    else:
                        if alertas_detectados:
                            st.warning("⚠️ " + txt("Condições que requerem avaliação profissional:", "Condiciones que requieren evaluación profesional:") + "\n\n" +
                                       "\n".join(alertas_detectados))
                        if info_detectados:
                            st.info("📎 " + txt("Informações adicionais para registro:", "Información adicional para el registro:") + "\n\n" +
                                    "\n".join(info_detectados))
                        st.success("✅ " + txt("Cliente apta para continuar — ficha validada com sucesso.", "Cliente apta para continuar — ficha validada correctamente."))
                        st.session_state.ficha_validada = True
                        
# 🔒 BLOQUEIO — Cliente apta?
if "cliente_apta" in st.session_state and st.session_state.cliente_apta == False:
    st.error("❌ Cliente não está apta para atendimento. Reação alérgica ou condição contraindicada.")
    st.stop()

# 1️⃣ Ficha de Anamnese
with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Ficha Clínica")):
    st.markdown("<h4 style='text-align:center;'>🧾 Ficha de Anamnese Clínica</h4>", unsafe_allow_html=True)
    # seu conteúdo da ficha permanece aqui como já implementado

# 2️⃣ Escolha do Efeito Lash
if st.session_state.ficha_validada:
    with st.expander(txt("✨ Escolha do Efeito Lash", "✨ Elección del Efecto Lash")):
        st.markdown("<h4 style='text-align:center;'>✨ Escolha do Efeito</h4>", unsafe_allow_html=True)

        efeitos = {
            "Clássica": {
                "img": "https://i.imgur.com/Nqrwdcm.png",
                "desc": txt("Fios distribuídos uniformemente — efeito natural e delicado",
                            "Fibras distribuidas uniformemente — efecto natural y delicado")
            },
            "Boneca": {
                "img": "https://i.imgur.com/vJUuvsl.png",
                "desc": txt("Maior concentração no centro — abre e arredonda o olhar",
                            "Mayor concentración en el centro — abre y redondea la mirada")
            },
            "Gatinho": {
                "img": "https://i.imgur.com/zpBFK0e.png",
                "desc": txt("Fios longos no canto externo — efeito sensual e alongado",
                            "Fibras largas en la esquina externa — efecto sensual y alargado")
            },
            "Esquilo": {
                "img": "https://i.imgur.com/BY5eEsr.png",
                "desc": txt("Volume acentuado entre o centro e canto externo — estilo marcante",
                            "Volumen acentuado entre el centro y la esquina externa — estilo llamativo")
            }
        }

        for nome, efeito in efeitos.items():
            col_img, col_txt = st.columns([2, 4])
            with col_img:
                st.image(efeito["img"], width=160)
            with col_txt:
                st.markdown(
                    f"<div style='text-align:center;'><h5>{nome}</h5><p>{efeito['desc']}</p></div>",
                    unsafe_allow_html=True
                )
                if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"efeito_{nome}"):
                    st.session_state.efeito_escolhido = nome
            st.divider()

        if "efeito_escolhido" in st.session_state:
            selecionado = st.session_state.efeito_escolhido
            st.success(txt(f"✅ Efeito selecionado: {selecionado}\n{efeitos[selecionado]['desc']}",
                           f"✅ Efecto seleccionado: {selecionado}\n{efeitos[selecionado]['desc']}"))

# 3️⃣ Tipo de Aplicação
if "efeito_escolhido" in st.session_state and st.session_state.efeito_escolhido is not None:
    with st.expander(txt("🎀 Tipo de Aplicação", "🎀 Tipo de Aplicación")):
        st.markdown("<h4 style='text-align:center;'>🎀 Tipo de Aplicação</h4>", unsafe_allow_html=True)

        tipos = {
            "Egípcio 3D": {
                "img": "https://i.imgur.com/TOPRWFQ.jpeg",
                "desc": txt("Fios em leque 3D com geometria precisa — efeito artístico, definido e sofisticado.",
                            "Fibras en abanico 3D con geometría precisa — efecto artístico, definido y sofisticado.")
            },
            "Volume Russo 4D": {
                "img": "https://i.imgur.com/tBX2O8e.jpeg",
                "desc": txt("Aplicação de 4 fios sintéticos por fio natural — resultado intenso, estruturado e glamouroso.",
                            "Aplicación de 4 fibras sintéticas por pestaña natural — resultado intenso, estructurado y glamoroso.")
            },
            "Volume Brasileiro": {
                "img": "https://i.imgur.com/11rw6Jv.jpeg",
                "desc": txt("Fios em formato Y. Traz volume leve e natural, respeitando a quantidade de fios naturais existentes.",
                            "Fibras en forma de Y. Aporta volumen ligero y natural, respetando la cantidad de pestañas naturales.")
            },
            "Fio a Fio": {
                "img": "https://i.imgur.com/VzlySv4.jpeg",
                "desc": txt("É aplicado 1 fio sintético sobre cada fio natural. Ideal para quem busca naturalidade com acabamento tipo rímel.",
                            "Se aplica 1 fibra sintética sobre cada pestaña natural. Ideal para quienes desean un acabado natural tipo máscara.")
            }
        }

        for nome, tipo in tipos.items():
            col_img, col_txt = st.columns([2, 4])
            with col_img:
                st.markdown(
                    f"<div style='text-align:center;'>"
                    f"<img src='{tipo['img']}' style='height:120px; width:160px; object-fit:cover; border-radius:6px;'>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with col_txt:
                st.markdown(
                    f"<div style='text-align:center;'><h5>{nome}</h5><p>{tipo['desc']}</p></div>",
                    unsafe_allow_html=True
                )
                if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"tipo_{nome}"):
                    st.session_state.tipo_aplicacao = nome
            st.divider()

        if "tipo_aplicacao" in st.session_state:
            selecionado = st.session_state.tipo_aplicacao
            st.success(txt(
                f"✅ Tipo selecionado: {selecionado}\n{tipos[selecionado]['desc']}",
                f"✅ Tipo seleccionado: {selecionado}\n{tipos[selecionado]['desc']}"
            ))
