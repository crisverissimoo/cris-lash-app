import streamlit as st
from datetime import datetime
import pytz

# 🪞 Configuração de página
st.set_page_config("Consultoria Cris Lash", layout="wide")

# 🌍 Data atual
fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()

# 🌐 Idioma
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.selectbox("🌐 Idioma / Language", ["Português", "Español"], key="idioma")

def txt(pt, es):
    return pt if st.session_state.get("idioma", "Português") == "Português" else es

# 🎀 Cabeçalho
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"<h2 style='text-align:center;'>💎 {txt('Sistema de Atendimento — Cris Lash','Sistema de Atención — Cris Lash')}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>📅 {txt('Hoje é','Hoy es')} <code>{hoje.strftime('%d/%m/%Y')}</code></p>", unsafe_allow_html=True)

# 💖 Boas-vindas
col1, col2, col3 = st.columns([0.5, 3, 0.5])
with col2:
    st.markdown(f"""
        <div style='
            text-align: center;
            background-color: #e8d1cb;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #c08081;
            margin-top: 10px;
            margin-bottom: 20px;
        '>
            <h3 style='color: #a7585c;'>{txt('Bem-vinda ao Cris Lash', 'Bienvenida a Cris Lash')}</h3>
            <p>{txt('Atendimento profissional com técnica em formação.',
                    'Atención profesional con técnica en formación.')}</p>
            <p style='font-weight: bold;'>{txt('Promoção: 10€ por aplicação!',
                                                '¡Promoción: 10€ por aplicación!')}</p>
        </div>
    """, unsafe_allow_html=True)

from datetime import datetime, timedelta

hoje = datetime.today().date()

# 🧠 Estados iniciais
if "acesso_admin" not in st.session_state:
    st.session_state.acesso_admin = False
if "historico_ocupados" not in st.session_state:
    st.session_state.historico_ocupados = []
if "historico_clientes" not in st.session_state:
    st.session_state.historico_clientes = []

# 🎯 Horários
def gerar_horarios():
    base = datetime.strptime("08:00", "%H:%M")
    return [(base + timedelta(minutes=30 * i)).strftime("%H:%M") for i in range(21)]

def esta_livre(data, horario):
    inicio = datetime.strptime(horario, "%H:%M")
    fim = inicio + timedelta(hours=2)
    for ag_data, ag_hora in st.session_state.historico_ocupados:
        ag_inicio = datetime.strptime(ag_hora, "%H:%M")
        ag_fim = ag_inicio + timedelta(hours=2)
        if data == ag_data and (
            (inicio >= ag_inicio and inicio < ag_fim) or
            (fim > ag_inicio and fim <= ag_fim) or
            (inicio <= ag_inicio and fim >= ag_fim)
        ):
            return False
    return True

# 🔐 Área profissional + painel
# 🔐 Área profissional + painel
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.expander("👑 Área profissional", expanded=True):
        st.markdown("### 🔐 Acesso restrito")
        st.write("Digite o código secreto para liberar o painel de administração.")
        codigo_digitado = st.text_input("🔐 Código de acesso", type="password")
        if st.button("🔓 Entrar"):
            if codigo_digitado.strip().lower() == "rainha":
                st.session_state.acesso_admin = True
                st.success("💎 Acesso profissional liberado!")
            else:
                st.error("❌ Código inválido — tente novamente.")

        if st.session_state.get("acesso_admin"):
            import json
            import os
            from datetime import datetime

            st.markdown("---")
            st.markdown("## 👑 Painel Administrativo Boutique")

            # Carrega atendimentos
            CAMINHO_ARQUIVO = "agenda.json"
            clientes_salvos = []
            if os.path.exists(CAMINHO_ARQUIVO):
                with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
                    clientes_salvos = json.load(f)

            st.markdown("### 📋 Atendimentos em ordem de protocolo")
            if clientes_salvos:
                clientes_salvos.sort(key=lambda c: c["protocolo"])
                for idx, cliente in enumerate(clientes_salvos):
                    with st.container():
                        st.markdown(f"""
                            <div style='
                                background-color: #d495a2;
                                padding:15px;
                                border-left:5px solid #cc4c73;
                                border-radius:8px;
                                font-size:15px;
                                margin-bottom:10px;
                            '>
                                <strong>🔢 Protocolo:</strong> {cliente['protocolo']}<br>
                                <strong>🧍 Nome:</strong> {cliente['nome']}<br>
                                <strong>✨ Efeito:</strong> {cliente['efeito']}<br>
                                <strong>🎀 Técnica:</strong> {cliente['tipo']} — 💶 {cliente['valor']}<br>
                                <strong>📅 Data:</strong> {cliente['data']}<br>
                                <strong>⏰ Horário:</strong> {cliente['horario']}<br>
                                <strong>💬 Mensagem:</strong> {cliente['mensagem'] or '—'}
                            </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"❌ Excluir protocolo {cliente['protocolo']}", key=f"excluir_{idx}"):
                            confirmacao = st.radio(
                                f"⚠️ Tem certeza que deseja excluir o protocolo {cliente['protocolo']}?",
                                ["Cancelar", "Confirmar"],
                                key=f"confirmar_{idx}"
                            )
                            if confirmacao == "Confirmar":
                                clientes_salvos.pop(idx)
                                with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
                                    json.dump(clientes_salvos, f, ensure_ascii=False, indent=2)
                                st.success("✅ Atendimento excluído com sucesso!")
                                st.experimental_rerun()
            else:
                st.info("📂 Nenhum atendimento registrado ainda.")

            # Horários ocupados
            st.markdown("### 📅 Horários ocupados")
            if st.session_state.historico_ocupados:
                agenda = {}
                for data, hora in st.session_state.historico_ocupados:
                    d_str = data.strftime('%d/%m/%Y')
                    agenda.setdefault(d_str, []).append(hora)
                for dia, horas in agenda.items():
                    st.markdown(f"**📅 {dia}**: {' | '.join(sorted(horas))}")
            else:
                st.info("📂 Nenhum horário bloqueado ainda.")

            # Bloqueio e desbloqueio
            with st.expander("🚫 Bloquear período"):
                hoje = datetime.today().date()
                dia_bloqueio = st.date_input("📅 Data para bloquear/desbloquear", value=hoje, key="bloqueio_data")

                tipo_bloqueio = st.radio("Qual período deseja bloquear?", ["⏰ Horário único", "🌅 Manhã completa", "🌇 Tarde completa"], key="tipo_bloqueio")

                if tipo_bloqueio == "⏰ Horário único":
                    hora_bloqueio = st.selectbox("⏰ Horário", gerar_horarios(), key="bloqueio_hora")
                    if st.button("🚫 Confirmar bloqueio de horário", key="confirmar_horario_unico"):
                        if esta_livre(dia_bloqueio, hora_bloqueio):
                            st.session_state.historico_ocupados.append((dia_bloqueio, hora_bloqueio))
                            st.success(f"✅ Horário {hora_bloqueio} bloqueado em {dia_bloqueio.strftime('%d/%m/%Y')}.")
                        else:
                            st.warning("⚠️ Esse horário já está ocupado.")

                elif tipo_bloqueio == "🌅 Manhã completa":
                    if st.button("🚫 Confirmar bloqueio da manhã", key="confirmar_manha"):
                        manha = ["08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30"]
                        bloqueados = [h for h in manha if esta_livre(dia_bloqueio, h)]
                        for h in bloqueados:
                            st.session_state.historico_ocupados.append((dia_bloqueio, h))
                        if bloqueados:
                            st.success(f"✅ Manhã bloqueada ({', '.join(bloqueados)}) em {dia_bloqueio.strftime('%d/%m/%Y')}.")
                        else:
                            st.warning("⚠️ Todos os horários da manhã já estavam ocupados.")

                elif tipo_bloqueio == "🌇 Tarde completa":
                    if st.button("🚫 Confirmar bloqueio da tarde", key="confirmar_tarde"):
                        tarde = ["13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]
                        bloqueados = [h for h in tarde if esta_livre(dia_bloqueio, h)]
                        for h in bloqueados:
                            st.session_state.historico_ocupados.append((dia_bloqueio, h))
                        if bloqueados:
                            st.success(f"✅ Tarde bloqueada ({', '.join(bloqueados)}) em {dia_bloqueio.strftime('%d/%m/%Y')}.")
                        else:
                            st.warning("⚠️ Todos os horários da tarde já estavam ocupados.")

                # Desbloqueio manual
                st.markdown("### 🔓 Desbloquear horário manual")
                bloqueios_atuais = [(d, h) for (d, h) in st.session_state.historico_ocupados if d == dia_bloqueio]
                if bloqueios_atuais:
                    hora_desbloqueio = st.selectbox("⏰ Selecione um horário bloqueado para remover", [h for _, h in bloqueios_atuais], key="desbloqueio_hora")
                    if st.button("🔓 Confirmar remoção de bloqueio", key="remover_bloqueio"):
                        st.session_state.historico_ocupados = [(d, h) for (d, h) in st.session_state.historico_ocupados if not (d == dia_bloqueio and h == hora_desbloqueio)]
                        st.success(f"✅ Bloqueio removido para {hora_desbloqueio} em {dia_bloqueio.strftime('%d/%m/%Y')}.")
                else:
                    st.info("📂 Nenhum horário bloqueado neste dia.")

            # Gerenciar atendimentos
            st.markdown("### 🧍 Gerenciar atendimentos")
            if st.session_state.historico_clientes:
                nomes = [c["nome"] for c in st.session_state.historico_clientes]
                selecionada = st.selectbox("🧍 Escolha uma cliente", nomes, key="cliente_escolhida")
                cliente = next((c for c in st.session_state.historico_clientes if c["nome"] == selecionada), None)
                if cliente:
                    st.markdown(f"""
                        <div style='
                            background-color: #f4e3e5;
                            padding:15px;
                            border-left:4px solid #b4637d;
                            border-radius:8px;
                            font-size:15px;
                            margin-bottom:10px;







# 🧠 Estados iniciais
for key in ["ficha_validada", "cliente_apta", "efeito_escolhido", "tipo_aplicacao", "valor", "agendamento_confirmado", "cadastro_completo"]:
    if key not in st.session_state:
        st.session_state[key] = None
for key in ["historico_ocupados", "historico_clientes", "protocolo"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key != "protocolo" else 1

# 🗂️ Cadastro da Cliente
from datetime import datetime

hoje = datetime.today().date()

# 🔐 Inicializa a trava se não existir
if "cadastro_completo" not in st.session_state:
    st.session_state.cadastro_completo = False

# 🗂️ Cadastro da Cliente
from datetime import datetime

hoje = datetime.today().date()

# 🔐 Inicializa controle único
if "cadastro_confirmado" not in st.session_state:
    st.session_state.cadastro_confirmado = False

# 🗂️ Cadastro da Cliente
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.expander(txt("🗂️ Cadastro da Cliente", "🗂️ Registro de Cliente"), expanded=True):
        st.markdown("<h4 style='text-align:center;'>🗂️ Cadastro da Cliente</h4>", unsafe_allow_html=True)

        nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"))
        nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                                   min_value=datetime(1920, 1, 1).date(), max_value=hoje)
        telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"))
        email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"))

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.info(f"📌 {txt('Idade:', 'Edad:')} **{idade} {txt('anos', 'años')}**")

        autorizada = True
        if menor:
            responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"))
            autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"),
                                   ["Sim", "Não", "Pendente"], index=None)
            if autorizacao != "Sim":
                st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.",
                             "❌ Cliente menor sin autorización — atención bloqueada."))
                autorizada = False

        # ⚠️ Mensagem de erro se clicar sem preencher tudo
        if st.button(txt("✅ Confirmar cadastro", "✅ Confirmar registro")):
            campos_ok = nome and telefone and nascimento and idade >= 0
            if menor:
                campos_ok = campos_ok and autorizada

            if campos_ok:
                st.session_state.nome_cliente = nome
                st.session_state.nascimento = nascimento
                st.session_state.telefone = telefone
                st.session_state.email = email
                st.session_state.idade_cliente = idade
                st.session_state.cadastro_confirmado = True
                st.success(txt("✅ Cadastro finalizado com sucesso!",
                               "✅ Registro completado con éxito!"))
            else:
                st.warning(txt("⚠️ Preencha todos os dados corretamente para continuar.",
                               "⚠️ Rellena correctamente todos los campos para continuar."))



# só segue adiante se cadastro_completo estiver marcado como True

if st.session_state.get("cadastro_confirmado"):

    col_apl1, col_apl2, col_apl3 = st.columns([1, 2, 1])
    with col_apl2:
        with st.expander(txt("🎀 Aplicação + Técnica", "🎀 Aplicación + Técnica"), expanded=True):

            efeito = st.selectbox(txt("✨ Efeito desejado", "✨ Efecto deseado"),
                                  ["Clássico", "Híbrido", "Volume Russo"], key="efeito_escolhido")

            tipo = st.radio(txt("Tipo de aplicação", "Tipo de aplicación"),
                            ["Nova aplicação", "Manutenção"], key="tipo_aplicacao")

            precos = {"Clássico": 28, "Híbrido": 32, "Volume Russo": 37}
            valor = precos.get(efeito, 30)
            if tipo == "Manutenção":
                valor = valor - 8
            st.session_state.valor = valor

            st.success(f"{txt('💶 Valor final:', '💶 Precio final:')} **{valor} €**")

            horario = st.time_input(txt("⏰ Horário desejado", "⏰ Horario deseado"), key="horario_aplicacao")
            confirmar = st.checkbox(txt("Confirmar atendimento para esse horário",
                                        "Confirmar cita para esta hora"), key="confirma_agendamento")

            if confirmar:
                st.session_state.agendamento_confirmado = True

                protocolo = st.session_state.protocolo
                st.session_state.protocolo += 1

                cliente = {
                    "Protocolo": protocolo,
                    "Nome": nome,
                    "Idade": idade,
                    "Telefone": telefone,
                    "Email": email,
                    "Efeito": efeito,
                    "Tipo": tipo,
                    "Valor": valor,
                    "Horário": str(horario.strftime('%H:%M'))
                }
                st.session_state.historico_clientes.append(cliente)
                st.session_state.historico_ocupados.append(str(horario))

                st.success(txt("📝 Atendimento registrado no histórico.",
                               "📝 Atención registrada en el historial."))

                texto = txt(
                    f"Olá {nome}! 🌸 Sua aplicação {efeito} ({tipo}) está confirmada para {horario.strftime('%H:%M')} na Cris Lash. Valor: {valor}€.",
                    f"Hola {nome}! 🌸 Tu aplicación {efeito} ({tipo}) está confirmada para las {horario.strftime('%H:%M')} en Cris Lash. Precio: {valor}€."
                )

                link = f"https://wa.me/?text={texto.replace(' ', '%20')}"
                st.markdown(f"[📲 {txt('Enviar no WhatsApp', 'Enviar por WhatsApp')}]({link})", unsafe_allow_html=True)




# 🔁 Reprogramação de cliente
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.expander(txt("🔁 Reprogramar cliente", "🔁 Reprogramar cliente"), expanded=False):
        if st.session_state.historico_clientes:
            selecionada = st.selectbox("📍 Escolha cliente:", [c["Nome"] for c in st.session_state.historico_clientes], key="cliente_reprograma")
            novo_horario = st.time_input("⏰ Novo horário")

            if st.button(txt("📅 Reprogramar aplicação", "📅 Reprogramar aplicación")):
                st.success(txt(f"✅ {selecionada} reprogramada para {novo_horario.strftime('%H:%M')}",
                               f"✅ {selecionada} reprogramada para las {novo_horario.strftime('%H:%M')}"))



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
                <img src="{tipo['img']}" alt="{nome}" style="width: 100%; border-radius: 8px;">
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



# 🗓️ Etapa final — Agendamento
from datetime import datetime, timedelta
import os
import json

if st.session_state.get("efeito_escolhido") and st.session_state.get("tipo_aplicacao"):

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.expander("📅 Agendamento do Atendimento", expanded=True):

            data = st.date_input(
                "📅 Escolha a data do atendimento",
                min_value=datetime.today().date()
            )

            horarios_livres = [
                h for h in gerar_horarios()
                if esta_livre(data, h)
            ]

            if not horarios_livres:
                st.warning("⛔ Nenhum horário disponível neste dia.")
            else:
                horario = st.selectbox("🕐 Escolha o horário", horarios_livres)
                fim = (
                    datetime.strptime(horario, "%H:%M") + timedelta(hours=2)
                ).strftime("%H:%M")

                nome = st.session_state.get("nome_cliente", "—")
                efeito = st.session_state.get("efeito_escolhido", "—")
                tipo = st.session_state.get("tipo_aplicacao", "—")
                valor = st.session_state.get("valor", "—")
                mensagem = st.text_area(
                    "📩 Mensagem adicional (opcional)",
                    placeholder="Ex: alergia, dúvidas..."
                )

                st.markdown("💖 Confirme os dados do atendimento abaixo:")
                st.markdown(f"- 🧍 Nome: **{nome}**")
                st.markdown(f"- ✨ Efeito: **{efeito}**")
                st.markdown(f"- 🎀 Técnica: **{tipo}** — 💶 **{valor}**")
                st.markdown(f"- 📅 Data: `{data.strftime('%d/%m/%Y')}` — 🕐 Horário: `{horario}` → `{fim}`")
                st.markdown(f"- 💬 Mensagem: `{mensagem or '—'}`")

                if st.button("✅ Confirmar atendimento", key="confirmar_atendimento_unico"):
                    protocolo = st.session_state.protocolo
                    st.session_state.protocolo += 1

                    cliente = {
                        "protocolo": protocolo,
                        "efeito": efeito,
                        "tipo": tipo,
                        "valor": valor,
                        "data": data.strftime('%d/%m/%Y'),
                        "horario": f"{horario} → {fim}",
                        "mensagem": mensagem,
                        "nome": nome
                    }

                    CAMINHO_ARQUIVO = "agenda.json"
                    dados_existentes = []
                    if os.path.exists(CAMINHO_ARQUIVO):
                        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
                            dados_existentes = json.load(f)

                    dados_existentes.append(cliente)
                    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
                        json.dump(dados_existentes, f, ensure_ascii=False, indent=2)

                    st.session_state.historico_clientes.append(cliente)
                    st.session_state.historico_ocupados.append((data, horario))
                    st.session_state.agendamento_confirmado = True

                    st.success("✅ Atendimento agendado e salvo com sucesso!")

                    cuidados_html = """\
                   <div style="border: 2px dashed #e09b8e; background-color: #c08081;
                   border-radius: 10px; padding: 20px; margin-top: 20px; color: white;">
                   <h5>📌 Cuidados antes e depois da aplicação</h5>
                   <ul>
                    <li>🚫 Compareça sem maquiagem nos olhos</li>
                   <li>🧼 Lave o rosto com sabonete neutro antes do procedimento</li>
                    <li>🕐 Evite molhar os cílios por 24h após aplicação</li>
                    <li>🌙 Dormir de barriga para cima ajuda a preservar os fios</li>
                    <li>💧 Use apenas produtos oil-free na região dos olhos</li>
                   </ul>
                   </div>
                   """
                    st.markdown(cuidados_html, unsafe_allow_html=True)




