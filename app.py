import streamlit as st
from datetime import datetime, date, timedelta
import pytz

# 🕐 Configuração de data e página
fuso = pytz.timezone("Europe/Madrid")
hoje = datetime.now(fuso).date()
st.set_page_config("Consultoria Cris Lash", layout="wide")

# 🌐 Função de idioma
def txt(pt, es): return pt if st.session_state.get("idioma", "Português") == "Português" else es

# 🔧 Estados iniciais
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

# 👤 Cadastro da cliente
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("---")
    st.markdown("<h4 style='text-align:center;'>🧍 Cadastro da Cliente</h4>", unsafe_allow_html=True)

    nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"))
    nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                               min_value=date(1920, 1, 1), max_value=hoje)
    telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"))
    email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"))

    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"📌 {txt('Idade:','Edad:')} **{idade} {txt('anos','años')}**")

    autorizacao = "Sim"
    if idade < 18:
        responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"))
        autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"), ["Sim", "Não", "Pendente"])
        if autorizacao != "Sim":
            st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.", "❌ Cliente menor sin autorización — atención bloqueada."))

# 🎯 Validação do cadastro
cadastro_ok = (
    nome.strip() != "" and telefone.strip() != "" and
    (idade >= 18 or (idade < 18 and autorizacao == "Sim"))
)

# 🧾 Ficha clínica só aparece se cadastro estiver completo e válido
col_esq, col_centro, col_dir = st.columns([1, 2, 1])
with col_centro:
    if cadastro_ok:
        st.markdown("---")
        st.markdown("<h4 style='text-align:center;'>🧾 Ficha Clínica</h4>", unsafe_allow_html=True)
        
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

            respostas = {}
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
                    if avis: st.warning("⚠️ " + txt("Requer atenção:", "Requiere atención:") + "\n\n" + "\n".join(avis))
                    if inf: st.info("📎 " + txt("Informações adicionais:", "Información adicional:") + "\n\n" + "\n".join(inf))
                    st.success("✅ " + txt("Cliente apta — ficha validada!", "Cliente apta — ficha validada!"))
                    st.session_state.ficha_validada = True
                    st.session_state.cliente_apta = True
    else:
        st.markdown("""
        <div style='
            background-color:#e8f4fc;
            padding:8px 12px;
            border-radius:6px;
            border-left:4px solid #539dcd;
            color:#222;
            text-align:center;
            font-size:15px;
            max-width:400px;
            margin:auto;
        '>
        📌 <strong>Complete o cadastro corretamente para liberar a ficha clínica.</strong>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.get("ficha_validada") and st.session_state.get("cliente_apta"):

    # 💫 Título
    col_e, col_c, col_d = st.columns([1, 2, 1])
    with col_c:
        st.markdown("<h4 style='text-align:center;'>✨ Escolha o Efeito Lash</h4>", unsafe_allow_html=True)

    # 🌟 Lista de efeitos
    efeitos = {
        "Clássica": {
            "img": "https://i.imgur.com/Nqrwdcm.png",
            "desc": txt("Fios distribuídos uniformemente — efeito natural e delicado", "Fibras distribuidas uniformemente — efecto natural y delicado"),
            "tipo_olho": txt("Olhos amendoados ou simétricos", "Ojos almendrados o simétricos")
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
        },
        "Esquilo": {
            "img": "https://i.imgur.com/BY5eEsr.png",
            "desc": txt("Volume acentuado entre centro e canto externo — estilo marcante", "Volumen entre centro y esquina externa — estilo llamativo"),
            "tipo_olho": txt("Olhos puxados ou olhos grandes", "Ojos rasgados o grandes")
        }
    }

    for nome, efeito in efeitos.items():
        col_e, col_c, col_d = st.columns([1, 2, 1])
        with col_c:
            # 🔲 Card centralizado
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            st.image(efeito["img"], width=400)
            st.markdown(f"<h5>🎀 {txt(f'Efeito {nome}', f'Efecto {nome}')}</h5>", unsafe_allow_html=True)
            st.write(efeito["desc"])
            st.caption(f"👁️ {txt('Indicado para:', 'Indicado para:')} {efeito['tipo_olho']}")

            # 🔘 Botão simples
            if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"btn_{nome}"):
                st.session_state.efeito_escolhido = nome
            st.markdown("</div>", unsafe_allow_html=True)

        # 🌬️ Espaço entre cards
        st.markdown("<br>", unsafe_allow_html=True)

    # ✅ Confirmação
    if st.session_state.get("efeito_escolhido"):
        nome = st.session_state.efeito_escolhido
        col_e, col_c, col_d = st.columns([1, 2, 1])
        with col_c:
            st.success("✅ " + txt(
                f"Efeito selecionado: {nome}\n{efeitos[nome]['desc']}",
                f"Efecto seleccionado: {nome}\n{efeitos[nome]['desc']}"
            ))


        
 # 💅 Escolha do Tipo de Aplicação
# 💅 Escolha do Tipo de Aplicação
# 💅 Tipo de Aplicação — em duas colunas
col_esq, col_centro, col_dir = st.columns([1, 2, 1])
with col_centro:
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
            "desc": txt("Fios Y — volume leve e natural.",
                        "Fibras en Y — volumen ligero y natural."),
            "valor": "10€"
        },
        "Fio a Fio": {
            "img": "https://i.imgur.com/VzlySv4.jpeg",
            "desc": txt("1 fio por cílio — acabamento natural tipo rímel.",
                        "1 fibra por pestaña — acabado natural tipo máscara."),
            "valor": "10€"
        }
    }

    nomes = list(tipos.keys())
for i in range(0, len(nomes), 2):
    col1, col2 = st.columns(2)
    for j, col in enumerate([col1, col2]):
        if i + j < len(nomes):
            nome = nomes[i + j]
            tipo = tipos[nome]
            with col:
                st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
                st.image(tipo["img"], width=220)  # 🔧 padronizado para todas
                st.markdown(f"<h5>🎀 {nome} — 💶 {tipo['valor']}</h5>", unsafe_allow_html=True)
                st.caption(tipo["desc"])
                if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"tipo_{nome}"):
                    st.session_state.tipo_aplicacao = nome
                    st.session_state.valor = tipo["valor"]
                st.markdown("</div>", unsafe_allow_html=True)


    # ✅ Bloqueia próxima etapa até que escolha seja feita
    if st.session_state.get("tipo_aplicacao"):
        selecionado = st.session_state.tipo_aplicacao
        st.success(txt(f"✅ Tipo selecionado: {selecionado}", f"✅ Tipo seleccionado: {seleccionado}"))
    else:
        st.warning(txt("👀 Selecione uma aplicação para continuar.", "👀 Selecciona un tipo para continuar."))


        # 💅 Selecionei o tipo — agora libera o agendamento
        col_e, col_centro, col_d = st.columns([1, 2, 1])
        with col_centro:
            st.markdown("<h4 style='text-align:center;'>📅 Agendamento</h4>", unsafe_allow_html=True)
            data = st.date_input(txt("📆 Escolha a data", "📆 Selecciona la fecha"), min_value=hoje)

            def gerar_horarios():
                base = datetime.strptime("08:00", "%H:%M")
                return [(base + timedelta(minutes=30 * i)).strftime("%H:%M") for i in range(21)]

            def esta_livre(data, horario):
                inicio = datetime.strptime(horario, "%H:%M")
                fim = inicio + timedelta(hours=2)
                for ag_data, ag_hora in st.session_state.historico_ocupados:
                    if data == ag_data:
                        ag_inicio = datetime.strptime(ag_hora, "%H:%M")
                        ag_fim = ag_inicio + timedelta(hours=2)
                        if inicio < ag_fim and fim > ag_inicio:
                            return False
                return True

            horarios_disponiveis = [h for h in gerar_horarios() if esta_livre(data, h)]

            if not horarios_disponiveis:
                st.warning("⛔ Nenhum horário disponível neste dia.")
            else:
                horario = st.selectbox(txt("🕐 Horário", "🕐 Horario"), horarios_disponiveis)
                hora_fim = (datetime.strptime(horario, "%H:%M") + timedelta(hours=2)).strftime("%H:%M")
                efeito = st.session_state.efeito_escolhido
                tipo = st.session_state.tipo_aplicacao
                valor = st.session_state.valor

                st.markdown(f"💖 Serviço: **{efeito} + {tipo}** — 💶 {valor}")
                st.markdown(f"📅 Data: `{data.strftime('%d/%m/%Y')}` — ⏰ `{horario} às {hora_fim}`")

                mensagem = st.text_area("📩 Mensagem para Cris (opcional)", placeholder="Ex: tenho alergia, favor confirmar")

                if st.button("✅ Confirmar atendimento"):
                    st.session_state.agendamento_confirmado = True
                    st.session_state.historico_ocupados.append((data, horario))
                    st.success("✅ Atendimento agendado com sucesso!")

                    st.markdown("""
                        <div style='border: 2px dashed #e09b8e; background-color: #fffaf8; border-radius: 10px; padding: 20px; margin-top: 20px;'>
                            <h5>📌 Cuidados antes e depois da aplicação</h5>
                            <ul style='text-align:left;'>
                                <li>🚫 Compareça sem maquiagem nos olhos</li>
                                <li>🧼 Lave o rosto com sabonete neutro antes do procedimento</li>
                                <li>🕐 Evite molhar os cílios por 24h após aplicação</li>
                                <li>🌙 Dormir de barriga para cima ajuda a preservar os fios</li>
                                <li>💧 Use apenas produtos oil-free na região dos olhos</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
