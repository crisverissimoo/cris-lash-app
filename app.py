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

if autorizada:
    with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Ficha Clínica")):
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

                respostas = {}
                for chave, pergunta in perguntas.items():
                    col_a, col_b, col_c = st.columns([1, 4, 1])
                    with col_b:
                        respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

                col_botao_esq, col_botao_centro, col_botao_dir = st.columns([1, 2, 1])
                with col_botao_centro:
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

                        
# 🎯 Bloco 1 — Escolha do Efeito (liberado após ficha validada)
if st.session_state.ficha_validada:
    with st.expander(txt("✨ Escolha do Efeito Lash", "✨ Elección del Efecto Lash")):
        col_esq, col_centro, col_dir = st.columns([1, 2, 1])
        with col_centro:
            st.markdown("<h4 style='text-align:center;'>✨ Escolha o Efeito</h4>", unsafe_allow_html=True)

            efeitos = {
                "Clássica": {
                    "img": "https://i.imgur.com/Nqrwdcm.png",
                    "desc": txt("Fios distribuídos uniformemente — efeito natural e delicado", "Fibras distribuidas uniformemente — efecto natural y delicado")
                },
                "Boneca": {
                    "img": "https://i.imgur.com/vJUuvsl.png",
                    "desc": txt("Maior concentração no centro — abre e arredonda o olhar", "Mayor concentración en el centro — abre y redondea la mirada")
                },
                "Gatinho": {
                    "img": "https://i.imgur.com/zpBFK0e.png",
                    "desc": txt("Fios longos no canto externo — efeito sensual e alongado", "Fibras largas en la esquina externa — efecto sensual y alargado")
                },
                "Esquilo": {
                    "img": "https://i.imgur.com/BY5eEsr.png",
                    "desc": txt("Volume acentuado entre o centro e canto externo — estilo marcante", "Volumen acentuado entre el centro y la esquina externa — estilo llamativo")
                }
            }

            col1, col2 = st.columns(2)
            lado_esq = list(efeitos.keys())[:2]
            lado_dir = list(efeitos.keys())[2:]

            for col, nomes in zip([col1, col2], [lado_esq, lado_dir]):
                with col:
                    for nome in nomes:
                        efeito = efeitos[nome]
                        st.image(efeito["img"], caption=txt(f"Técnica {nome}", f"Técnica {nome}"), use_container_width=True)
                        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
                        label = txt(f"Selecionar {nome}: {efeito['desc']}", f"Seleccionar {nome}: {efeito['desc']}")
                        if st.button(label, key=f"btn_{nome}"):
                            st.session_state.efeito_escolhido = nome
                        st.markdown("</div>", unsafe_allow_html=True)

            if "efeito_escolhido" in st.session_state:
                selecionado = st.session_state.efeito_escolhido
                st.success(txt(
                    f"✅ Efeito selecionado: {selecionado}\n{efeitos[selecionado]['desc']}",
                    f"✅ Efecto seleccionado: {selecionado}\n{efeitos[selecionado]['desc']}"
                ))

# 🎯 Bloco 2 — Escolha do Tipo (liberado somente após escolher o efeito)
if "efeito_escolhido" in st.session_state:
    with st.expander(txt("🎀 Escolha o Tipo de Aplicação", "🎀 Elige el Tipo de Aplicación")):
        col_esq, col_centro, col_dir = st.columns([1, 2, 1])
        with col_centro:
            st.markdown("<h4 style='text-align:center;'>🎀 Tipo de Aplicação</h4>", unsafe_allow_html=True)

            tipos = {
                "Fio a Fio": {
                    "img": "https://i.imgur.com/8Xz3vJv.jpg",
                    "desc": txt(
                        "É aplicado 1 fio sintético sobre cada fio natural. Ideal para quem busca naturalidade com acabamento tipo rímel.",
                        "Se aplica 1 fibra sintética sobre cada pestaña natural. Ideal para quienes desean un acabado natural tipo máscara."
                    )
                },
                "Volume Brasileiro": {
                    "img": "https://i.imgur.com/3Yz9bqK.jpg",
                    "desc": txt(
                        "Fios em formato Y. O volume depende da quantidade de fios naturais — traz volume e leveza com naturalidade.",
                        "Fibras en forma de Y. El volumen varía según la cantidad de pestañas naturales — aporta volumen y naturalidad."
                    )
                },
                "Híbrido": {
                    "img": "https://i.imgur.com/2ZQvZzG.jpg",
                    "desc": txt(
                        "Combina Fio a Fio com Volume — equilíbrio entre leveza e densidade para um olhar marcante e suave.",
                        "Combina Fio a Fio con Volumen — equilibrio entre ligereza y densidad para una mirada llamativa y suave."
                    )
                },
                "Egípcio": {
                    "img": "https://i.imgur.com/4XgYgqP.jpg",
                    "desc": txt(
                        "Fios em formato W aplicados com geometria precisa — resultado artístico, gráfico e sofisticado.",
                        "Fibras en forma de W aplicadas con geometría precisa — resultado artístico, gráfico y sofisticado."
                    )
                },
                "Volume Russo": {
                    "img": "https://i.imgur.com/5YwWwqR.jpg",
                    "desc": txt(
                        "Feixes densos de 4 a 6 fios por natural — proporciona olhar glamouroso, intenso e estruturado.",
                        "Racimos densos de 4 a 6 fibras por pestaña — proporciona una mirada glamorosa, intensa y estructurada."
                    )
                }
            }

            col1, col2 = st.columns(2)
            lado_esq = list(tipos.keys())[:3]
            lado_dir = list(tipos.keys())[3:]

            for col, nomes in zip([col1, col2], [lado_esq, lado_dir]):
                with col:
                    for nome in nomes:
                        tipo = tipos[nome]
                        st.markdown(
                            f"<img src='{tipo['img']}' alt='Imagem {nome}' style='height:260px; width:100%; object-fit:cover; border-radius:8px;'>",
                            unsafe_allow_html=True
                        )
                        st.markdown("<div style='text-align:center; margin-top:6px;'>", unsafe_allow_html=True)
                        label = txt(f"Selecionar {nome}: {tipo['desc']}", f"Seleccionar {nome}: {tipo['desc']}")
                        if st.button(label, key=f"tipo_{nome}"):
                            st.session_state.tipo_aplicacao = nome
                        st.markdown("</div>", unsafe_allow_html=True)

            if "tipo_aplicacao" in st.session_state:
                selecionado = st.session_state.tipo_aplicacao
                st.success(txt(
                    f"✅ Tipo selecionado: {selecionado}\n{tipos[selecionado]['desc']}",
                    f"✅ Tipo seleccionado: {selecionado}\n{tipos[selecionado]['desc']}"
                ))
