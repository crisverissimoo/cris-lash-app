import streamlit as st
from datetime import datetime
import pytz

fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

st.set_page_config("Consultoria Cris Lash", layout="wide")

# Estado inicial
if "historico" not in st.session_state:
    st.session_state.historico = []
if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None
if "ficha_validada" not in st.session_state:
    st.session_state.ficha_validada = False
if "cliente_apta" in st.session_state and st.session_state.cliente_apta == False:
    st.error("❌ Cliente não está apta para atendimento. Reação alérgica ou condição contraindicada.")
    st.stop()

# Idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    idioma = st.selectbox("🌐 Idioma / Language", ["Português", "Español"], key="idioma")
    def txt(pt, es): return pt if idioma == "Português" else es

    # 🎀 Mensagem de boas-vindas
    st.markdown(f"""
    <div style='
    background-color:#fff2f2;
    padding:20px;
    border-radius:10px;
    border-left:5px solid #e09b8e;
    color:#333;
    font-size:16px;
'>
👋 <strong>Bem-vinda ao Cris Lash!</strong><br>
✨ Atendimento profissional com técnica em formação.<br>
💶 Valor promocional de lançamento: <strong>10€</strong> por aplicação!
</div>
""", unsafe_allow_html=True)

    # Título + data
    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash','Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.write(f"📅 {txt('Hoje é','Hoy es')} `{hoje.strftime('%d/%m/%Y')}`")

    # Ficha da cliente
    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente")):
        st.markdown("<h4 style='text-align:center;'>🗂️ Cadastro da Cliente</h4>", unsafe_allow_html=True)

        nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"), key="nome_cliente")
        nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                                   min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"), key="telefone")
        email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"), key="email")

        # Cálculo da idade
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

# Continuação da validação após ficha pessoal
if autorizada:
    st.session_state.ficha_validada = True
    st.session_state.cliente_apta = True
    respostas = {}

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("<h4 style='text-align:center;'>🧾 " + txt("Ficha de Anamnese Clínica", "Ficha Clínica") + "</h4>", unsafe_allow_html=True)

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
            if any(r is None for r in respostas.values()):
                st.warning("⚠️ " + txt("Você precisa responder todas as perguntas antes de finalizar.", "Debe responder todas las preguntas antes de continuar."))
                st.session_state.ficha_validada = False
            else:
                impeditivos = {"glaucoma", "infeccao", "conjuntivite", "cirurgia", "reacao"}
                alertas = {"alergia", "irritacao", "gravida", "acido", "sensibilidade"}
                informativos = {"colirio", "lentes", "extensao"}

                bloqueios, avisos, infos = [], [], []

                for chave, resposta in respostas.items():
                    if resposta == "Sim":
                        if chave in impeditivos:
                            bloqueios.append(f"- {perguntas[chave]}")
                        elif chave in alertas:
                            avisos.append(f"- {perguntas[chave]}")
                        elif chave in informativos:
                            infos.append(f"- {perguntas[chave]}")

                if bloqueios:
                    st.error("❌ " + txt("Cliente não está apta para atendimento.", "Cliente no apta para atención") + "\n\n" + "\n".join(bloqueios))
                    st.session_state.ficha_validada = False
                    st.session_state.cliente_apta = False
                    st.stop()
                else:
                    if avisos:
                        st.warning("⚠️ " + txt("Condições que requerem avaliação profissional:", "Condiciones que requieren evaluación profesional:") + "\n\n" + "\n".join(avisos))
                    if infos:
                        st.info("📎 " + txt("Informações adicionais para registro:", "Información adicional para el registro:") + "\n\n" + "\n".join(infos))
                    st.success("✅ " + txt("Cliente apta para continuar — ficha validada com sucesso.", "Cliente apta para continuar — ficha validada correctamente."))
                    st.session_state.ficha_validada = True
                    st.session_state.cliente_apta = True


# 🔓 Etapa 2 — Escolha de Efeito
 
if st.session_state.ficha_validada:
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("""
            <div style='
                padding: 25px;
                margin-top: 20px;
                margin-bottom: 40px;
            '>
        """, unsafe_allow_html=True)

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
            st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

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

        if "efeito_escolhido" in st.session_state:
            nome = st.session_state.efeito_escolhido
            st.success("✅ " + txt(
                f"Efeito selecionado: {nome}\n{efeitos[nome]['desc']}",
                f"Efecto seleccionado: {nome}\n{efeitos[nome]['desc']}"
            ))

        st.markdown("</div>", unsafe_allow_html=True)

# 🎯 Bloco 2 — Escolha do Tipo (liberado somente após escolher o efeito)

# Só exibe o bloco se efeito_escolhido estiver definido

# 🎯 Escolha do Tipo de Aplicação (exibe só após definir efeito)
if "efeito_escolhido" in st.session_state and st.session_state.efeito_escolhido is not None:
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("""
            <div style='border: 1px solid #ccc; border-radius: 10px; padding: 25px; margin-top: 20px; margin-bottom: 40px;'>
        """, unsafe_allow_html=True)

        st.markdown("<h4 style='text-align:center;'>🎀 Tipo de Aplicação</h4>", unsafe_allow_html=True)

        tipos = {
            "Egípcio 3D": {
                "img": "https://i.imgur.com/TOPRWFQ.jpeg",
                "desc": txt("Fios em leque 3D com geometria precisa — efeito artístico e sofisticado.",
                            "Fibras en abanico 3D con geometría precisa — efecto artístico y sofisticado."),
                "valor": "10€"
            },
            "Volume Russo 4D": {
                "img": "https://i.imgur.com/tBX2O8e.jpeg",
                "desc": txt("4 fios por cílio — resultado glamouroso e intenso.",
                            "4 fibras por pestaña — resultado glamoroso e intenso."),
                "valor": "10€"
            },
            "Volume Brasileiro": {
                "img": "https://i.imgur.com/11rw6Jv.jpeg",
                "desc": txt("Fios em formato Y — volume leve e natural.",
                            "Fibras en forma de Y — volumen ligero y natural."),
                "valor": "10€"
            },
            "Fio a Fio": {
                "img": "https://i.imgur.com/VzlySv4.jpeg",
                "desc": txt("1 fio por cílio — acabamento natural tipo rímel.",
                            "1 fibra por pestaña — acabado natural tipo máscara."),
                "valor": "10€"
            }
        }

        for nome, tipo in tipos.items():
            col_img, col_txt = st.columns([1.4, 1.6])
            with col_img:
                st.image(tipo["img"], width=160)
            with col_txt:
                st.markdown(f"**{nome}** — 💶 {tipo['valor']}")
                st.caption(tipo["desc"])
                if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"tipo_{nome}"):
                    st.session_state.tipo_aplicacao = nome
                    st.session_state.valor = tipo["valor"]

        if "tipo_aplicacao" in st.session_state:
            selecionado = st.session_state.tipo_aplicacao
            st.success(txt(f"✅ Tipo selecionado: {selecionado}", f"✅ Tipo seleccionado: {selecionado}"))

        st.markdown("</div>", unsafe_allow_html=True)

# 🎯 Agenda (exibe se técnica foi definida)
if "efeito_escolhido" in st.session_state and st.session_state.get("tipo_aplicacao"):
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        st.markdown("""
            <div style='border: 1px solid #ccc; border-radius: 10px; padding: 25px; margin-top: 20px; margin-bottom: 40px;'>
        """, unsafe_allow_html=True)

        st.markdown("<h4 style='text-align:center;'>📅 Agendamento do Atendimento</h4>", unsafe_allow_html=True)

        hoje = datetime.date.today()
        data = st.date_input("📅 Escolha a data", min_value=hoje)

        def gerar_horarios():
            base = datetime.datetime.strptime("08:00", "%H:%M")
            return [(base + datetime.timedelta(minutes=30 * i)).strftime("%H:%M") for i in range(21)]

        horarios_ocupados = st.session_state.get("historico_ocupados", [])

        def esta_livre(data, horario):
            inicio = datetime.datetime.strptime(horario, "%H:%M")
            fim = inicio + datetime.timedelta(hours=2)
            for ag_data, ag_hora in horarios_ocupados:
                if data == ag_data:
                    ag_inicio = datetime.datetime.strptime(ag_hora, "%H:%M")
                    ag_fim = ag_inicio + datetime.timedelta(hours=2)
                    if inicio < ag_fim and fim > ag_inicio:
                        return False
            return True

        horarios = gerar_horarios()
        horarios_livres = [h for h in horarios if esta_livre(data, h)]

        if not horarios_livres:
            st.warning("⛔ Nenhum horário disponível neste dia.")
        else:
            horario = st.selectbox("🕐 Escolha o horário", horarios_livres)
            efeito = st.session_state.efeito_escolhido
            tipo = st.session_state.tipo_aplicacao
            valor = st.session_state.valor
            hora_fim = (datetime.datetime.strptime(horario, "%H:%M") + datetime.timedelta(hours=2)).strftime("%H:%M")

            st.markdown(f"💖 Serviço: **{efeito} + {tipo}** — 💶 {valor}")
            st.markdown(f"📅 {data.strftime('%d/%m/%Y')} — 🕐 `{horario} às {hora_fim}`")

            mensagem = st.text_area("📩 Mensagem para a Cris (opcional)", placeholder="Tenho alergia, preciso confirmar...")

            if st.button("✅ Confirmar atendimento"):
                st.session_state.agendamento_confirmado = True
                if "historico_ocupados" not in st.session_state:
                    st.session_state.historico_ocupados = []
                st.session_state.historico_ocupados.append((data, horario))

        if st.session_state.get("agendamento_confirmado"):
            st.success("✅ Atendimento agendado com sucesso!")

            st.markdown("""
                <div style='border: 2px dashed #e09b8e; background-color: #fffaf8; border-radius: 10px; padding: 20px; margin-top: 20px;'>
                    <h5>📌 Cuidados antes e depois da aplicação</h5>
                    <ul>
                        <li>🚫 Compareça sem maquiagem nos olhos</li>
                        <li>🧼 Lave o rosto com sabonete neutro antes do procedimento</li>
                        <li>🕐 Evite molhar os cílios por 24h após aplicação</li>
                        <li>🌙 Dormir de barriga para cima ajuda a preservar os fios</li>
                        <li>💧 Use apenas produtos oil-free na região dos olhos</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
