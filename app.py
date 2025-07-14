import streamlit as st
from datetime import datetime, date, timedelta
import pytz

# 🌍 Fuso horário e data atual
fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

# 🪞 Configuração de página
st.set_page_config("Consultoria Cris Lash", layout="wide")

# 🌐 Função de idioma
def txt(pt, es): return pt if st.session_state.get("idioma", "Português") == "Português" else es

# 🔁 Estados iniciais
for key in ["ficha_validada", "cliente_apta", "efeito_escolhido", "tipo_aplicacao", "valor", "agendamento_confirmado"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "historico_ocupados" not in st.session_state:
    st.session_state.historico_ocupados = []

# 🎀 Boas-vindas + idioma centralizado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.selectbox("🌐 Idioma / Language", ["Português", "Español"], key="idioma")

    st.markdown("""
        <div style='background-color:#fff2f2; padding:15px; border-radius:10px;
                    border-left:5px solid #e09b8e; color:#333; font-size:16px'>
            👋 <strong>Bem-vinda ao Cris Lash!</strong><br>
            ✨ Atendimento profissional com técnica em formação.<br>
            💶 Valor promocional de lançamento: <strong>10€</strong> por aplicação!
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash','Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>📅 {txt('Hoje é','Hoy es')} <code>{hoje.strftime('%d/%m/%Y')}</code></p>", unsafe_allow_html=True)

# 🔜 Continuação esperada: Ficha da Cliente com travamento por idade + autorização (Etapa 1.2)


# 🗂️ Cadastro da Cliente
col_cad1, col_cad2, col_cad3 = st.columns([1, 2, 1])
with col_cad2:
    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente"), expanded=True):
        st.markdown("<h4 style='text-align:center;'>🗂️ Cadastro da Cliente</h4>", unsafe_allow_html=True)

        nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"), key="nome_cliente")
        nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                                   min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"), key="telefone")
        email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"), key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.info(f"📌 {txt('Idade:','Edad:')} **{idade} {txt('anos','años')}**")

        autorizada = True
        if menor:
            responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"), key="responsavel")
            autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"),
                                   ["Sim", "Não", "Pendente"], index=None, key="aut_menor")

            if autorizacao != "Sim":
                st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.",
                             "❌ Cliente menor sin autorización — atención bloqueada."))
                autorizada = False

        if st.button(txt("✅ Confirmar cadastro", "✅ Confirmar registro")):
            if not nome or not telefone or idade < 0 or (menor and not autorizada):
                st.warning(txt("⚠️ Preencha os dados corretamente para prosseguir.",
                               "⚠️ Rellena correctamente para continuar."))
            else:
                st.session_state.cadastro_completo = True
                st.success(txt("✅ Cadastro finalizado com sucesso!",
                               "✅ Registro completado con éxito!"))


if autorizada:
    respostas = {}

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        with st.expander(txt("🧾 Ficha de Anamnese Clínica", "🧾 Historial de salud"), expanded=True):
            with st.form("form_clinica"):
                st.markdown("<h4 style='text-align:center;'>🧾 Ficha de Anamnese Clínica</h4>", unsafe_allow_html=True)

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
        with st.expander(txt("✨ Escolha o Efeito Lash", "✨ Elige el Efecto Lash"), expanded=True):
            st.markdown("<h4 style='text-align:center;'>✨ Efeito Lash</h4>", unsafe_allow_html=True)

            efeitos = {
                "Clássica": {
                    "img": "https://i.imgur.com/Nqrwdcm.png",
                    "desc": txt("Distribuição uniforme — efeito natural e delicado", "Distribución uniforme — efecto natural y delicado"),
                    "tipo_olho": txt("Olhos amendoado ou simétricos", "Ojos almendrados o simétricos")
                },
                "Boneca": {
                    "img": "https://i.imgur.com/vJUuvsl.png",
                    "desc": txt("Centro mais intenso — abre e arredonda o olhar", "Centro más intenso — abre y redondea la mirada"),
                    "tipo_olho": txt("Olhos pequenos, fechados ou orientais", "Ojos pequeños, cerrados u orientales")
                },
                "Gatinho": {
                    "img": "https://i.imgur.com/zpBFK0e.png",
                    "desc": txt("Alongado no canto externo — olhar sensual", "Alargado en la esquina — mirada sensual"),
                    "tipo_olho": txt("Olhos caídos ou arredondados", "Ojos caídos o redondeados")
                },
                "Esquilo": {
                    "img": "https://i.imgur.com/BY5eEsr.png",
                    "desc": txt("Volume entre centro e canto — estilo marcante", "Volumen entre el centro y la esquina — estilo llamativo"),
                    "tipo_olho": txt("Olhos puxados ou olhos grandes", "Ojos rasgados o grandes")
                }
            }

            for nome, efeito in efeitos.items():
                st.markdown("<hr style='margin-top:40px; margin-bottom:30px;'>", unsafe_allow_html=True)

                col_img, col_txt = st.columns([1.8, 1.2])  # 📸 imagem com mais espaço

                with col_img:
                    st.image(efeito["img"], width=500)  # imagem destacada

                with col_txt:
                    st.markdown(f"<h5 style='text-align:center;'>🎀 {txt('Efeito','Efecto')} {nome}</h5>", unsafe_allow_html=True)
                    st.caption(efeito["desc"])
                    st.caption("👁️ " + txt("Indicado para:", "Indicado para:") + f" **{efeito['tipo_olho']}**")

                    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
                    with col_b2:
                        if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"btn_{nome}"):
                            st.session_state.efeito_escolhido = nome

            if st.session_state.get("efeito_escolhido"):
                nome = st.session_state.efeito_escolhido
                st.success("✅ " + txt(
                    f"Efeito selecionado: {nome}",
                    f"Efecto seleccionado: {nome}"
                ))



# 🎯 Bloco 2 — Escolha do Tipo (liberado somente após escolher o efeito)

# Só exibe o bloco se efeito_escolhido estiver definido

if st.session_state.get("efeito_escolhido"):
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        with st.expander(txt("🎀 Tipo de Aplicação", "🎀 Técnica de aplicación"), expanded=True):
            st.markdown("<h4 style='text-align:center;'>🎀 Técnica de Aplicação</h4>", unsafe_allow_html=True)

            tipos = {
                "Egípcio 3D": {
                    "img": "https://i.imgur.com/TOPRWFQ.jpeg",
                    "desc": txt("Leque 3D artístico — acabamento definido e sofisticado.", "Abanico 3D artístico — acabado definido y sofisticado."),
                    "valor": "10€"
                },
                "Volume Russo 4D": {
                    "img": "https://i.imgur.com/tBX2O8e.jpeg",
                    "desc": txt("4 fios por cílio — volume intenso e estruturado.", "4 fibras por pestaña — volumen intenso y estructurado."),
                    "valor": "10€"
                },
                "Volume Brasileiro": {
                    "img": "https://i.imgur.com/11rw6Jv.jpeg",
                    "desc": txt("Formato Y — volumoso e natural.", "Formato Y — voluminoso y natural."),
                    "valor": "10€"
                },
                "Fio a Fio": {
                    "img": "https://i.imgur.com/VzlySv4.jpeg",
                    "desc": txt("1 fio por cílio — efeito rímel natural.", "1 fibra por pestaña — efecto natural tipo máscara."),
                    "valor": "10€"
                }
            }

            for nome, tipo in tipos.items():
                st.markdown("<hr style='margin-top:30px; margin-bottom:30px;'>", unsafe_allow_html=True)

                col_img, col_txt = st.columns([1.6, 1.4])
                with col_img:
                    st.markdown(f"""
                        <div style='text-align:center;'>
                            <img src='{tipo["img"]}' alt='{nome}' style='
                                width: 320px;
                                height: 200px;
                                object-fit: cover;
                                border-radius: 8px;
                            '>
                        </div>
                    """, unsafe_allow_html=True)

                with col_txt:
                    st.markdown(f"<h5 style='text-align:center;'>{nome} — 💶 {tipo['valor']}</h5>", unsafe_allow_html=True)
                    st.caption(tipo["desc"])

                    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
                    with col_b2:
                        if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"tipo_{nome}"):
                            st.session_state.tipo_aplicacao = nome
                            st.session_state.valor = tipo["valor"]

            if st.session_state.get("tipo_aplicacao"):
                selecionado = st.session_state.tipo_aplicacao
                st.success(txt(
                    f"✅ Tipo selecionado: {selecionado} — 💶 {tipos[selecionado]['valor']}",
                    f"✅ Técnica seleccionada: {selecionado} — 💶 {tipos[selecionado]['valor']}"
                ))



# Função para gerar horários disponíveis
def gerar_horarios():
    base = datetime.datetime.strptime("08:00", "%H:%M")
    horarios = [(base + datetime.timedelta(minutes=30 * i)).strftime("%H:%M") for i in range(21)]
    return horarios

# Função para verificar se horário está livre
def esta_livre(data, horario):
    inicio = datetime.datetime.strptime(horario, "%H:%M")
    fim = inicio + datetime.timedelta(hours=2)

    for ag_data, ag_hora in horarios_ocupados:
        ag_inicio = datetime.datetime.strptime(ag_hora, "%H:%M")
        ag_fim = ag_inicio + datetime.timedelta(hours=2)

        if data == ag_data and (
            (inicio >= ag_inicio and inicio < ag_fim) or
            (fim > ag_inicio and fim <= ag_fim)
        ):
            return False
    return True

# 🎯 Etapa Agenda
if "efeito_escolhido" in st.session_state and st.session_state.get("tipo_aplicacao"):

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:

        st.markdown("""
            <div style='border: 1px solid #ccc; border-radius: 10px; padding: 25px; margin-top: 20px; margin-bottom: 40px;'>
        """, unsafe_allow_html=True)

        st.markdown("<h4 style='text-align:center;'>📅 Agendamento do Atendimento</h4>", unsafe_allow_html=True)

        # 📅 Calendário
        hoje = datetime.date.today()
        data = st.date_input("📅 Escolha a data do atendimento", min_value=hoje)

        # 🕐 Horários livres
        horarios = gerar_horarios()
        horarios_livres = [h for h in horarios if esta_livre(data, h)]

        if not horarios_livres:
            st.warning("⛔ Nenhum horário disponível neste dia.")
        else:
            horario = st.selectbox("🕐 Escolha o horário", horarios_livres)

            efeito = st.session_state.efeito_escolhido
            tipo = st.session_state.tipo_aplicacao

            st.markdown(f"💖 Serviço escolhido: **{efeito} + {tipo}**")
            st.markdown(f"📅 Dia: `{data.strftime('%d/%m/%Y')}` — 🕐 Horário: `{horario}` até `{(datetime.datetime.strptime(horario, '%H:%M') + datetime.timedelta(hours=2)).strftime('%H:%M')}`")

            # 💬 Mensagem personalizada
            mensagem = st.text_area("📩 Deixe uma mensagem (opcional)", placeholder="Ex: tenho alergia, preciso de confirmação, etc.")

            # ✅ Confirmação
            if st.button("✅ Confirmar atendimento"):
                st.session_state.agendamento_confirmado = True
                horarios_ocupados.append((data, horario))

        # 📌 Mensagem pós confirmação
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
