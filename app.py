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

# 🎀 Idioma + boas-vindas + cadastro (centralizado)
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

    st.markdown("---")
    st.markdown("<h4 style='text-align:center;'>🧍 Cadastro da Cliente</h4>", unsafe_allow_html=True)

    nome = st.text_input(txt("🧍 Nome completo", "🧍 Nombre completo"))
    nascimento = st.date_input(txt("📅 Data de nascimento", "📅 Fecha de nacimiento"),
                               min_value=date(1920, 1, 1), max_value=hoje)
    telefone = st.text_input(txt("📞 Telefone", "📞 Teléfono"))
    email = st.text_input(txt("📧 Email (opcional)", "📧 Correo (opcional)"))

    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    st.write(f"📌 {txt('Idade:','Edad:')} **{idade} {txt('anos','años')}**")

    # 🔒 Autorização (se menor)
    autorizacao = "Sim"
    if idade < 18:
        responsavel = st.text_input(txt("👨‍👩‍👧 Nome do responsável", "👨‍👩‍👧 Nombre del responsable"))
        autorizacao = st.radio(txt("Autorização recebida?", "¿Autorización recibida?"), ["Sim", "Não", "Pendente"])
        if autorizacao != "Sim":
            st.error(txt("❌ Cliente menor sem autorização — atendimento bloqueado.", "❌ Cliente menor sin autorización — atención bloqueada."))

    # ✅ Validação do cadastro completo
    cadastro_ok = (
        nome and nascimento and telefone and
        (idade >= 18 or (idade < 18 and autorizacao == "Sim"))
    )

# 📌 Ficha só aparece se cadastro estiver completo
col_esq, col_centro, col_dir = st.columns([1, 2, 1])
with col_centro:
    if cadastro_ok:
        respostas = {}
        st.markdown("---")
        st.markdown("<h4 style='text-align:center;'>🧾 Ficha Clínica</h4>", unsafe_allow_html=True)
        with st.form("form_clinica"):
            perguntas = {
                "glaucoma": "Possui glaucoma?",
                "infeccao": "Tem infecções oculares?",
                "conjuntivite": "Conjuntivite recente?",
                "cirurgia": "Cirurgia ocular recente?",
                "reacao": "Reação alérgica anterior?",
                "alergia": "Histórico de alergias?",
                "gravida": "Está grávida ou amamentando?",
                "acido": "Tratamento com ácido?",
                "irritacao": "Olhos irritados?",
                "sensibilidade": "Sensibilidade a químicos?",
                "colirio": "Uso frequente de colírios?",
                "lentes": "Usa lentes de contato?",
                "extensao": "Já fez extensão antes?"
            }

            for chave, pergunta in perguntas.items():
                respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

            enviar = st.form_submit_button("📨 Finalizar ficha")

        if enviar:
            if any(r is None for r in respostas.values()):
                st.warning("⚠️ Responda todas as perguntas.")
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
                    st.error("❌ Cliente não está apta para atendimento.\n\n" + "\n".join(bloc))
                    st.session_state.ficha_validada = False
                    st.session_state.cliente_apta = False
                    st.stop()
                else:
                    if avis: st.warning("⚠️ Requer atenção:\n\n" + "\n".join(avis))
                    if inf: st.info("📎 Informações adicionais:\n\n" + "\n".join(inf))
                    st.success("✅ Cliente apta — ficha validada!")
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
        },
        "Esquilo": {
            "img": "https://i.imgur.com/BY5eEsr.png",
            "desc": txt("Volume acentuado entre centro e canto externo — estilo marcante", "Volumen entre centro y esquina externa — estilo llamativo"),
            "tipo_olho": txt("Olhos puxados ou olhos grandes", "Ojos rasgados o grandes")
        }
    }

    for nome, efeito in efeitos.items():
        col_img, col_txt = st.columns([1.6, 1.4])
        with col_img:
            st.image(efeito["img"], width=460)
        with col_txt:
            st.markdown(f"**{txt(f'Efeito {nome}', f'Efecto {nome}')}**")
            st.write(efeito["desc"])
            st.markdown("👁️ " + txt("Indicado para:", "Indicado para:") + f" **{efeito['tipo_olho']}**")
            if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"btn_{nome}"):
                st.session_state.efeito_escolhido = nome

    if st.session_state.get("efeito_escolhido"):
        nome = st.session_state.efeito_escolhido
        st.success("✅ " + txt(
            f"Efeito selecionado: {nome}\n{efeitos[nome]['desc']}",
            f"Efecto seleccionado: {nome}\n{efeitos[nome]['desc']}"
        ))

        # 💅 Escolha do Tipo de Aplicação
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

        if st.session_state.get("tipo_aplicacao"):
            selecionado = st.session_state.tipo_aplicacao
            st.success(txt(f"✅ Tipo selecionado: {selecionado}", f"✅ Tipo seleccionado: {selecionado}"))

            # 📅 Agendamento
            st.markdown("<h4 style='text-align:center;'>📅 Agendamento</h4>", unsafe_allow_html=True)
            data = st.date_input("📆 Escolha a data", min_value=date.today())

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
                horario = st.selectbox("🕐 Horário", horarios_disponiveis)
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
                            <ul>
                                <li>🚫 Compareça sem maquiagem nos olhos</li>
                                <li>🧼 Lave o rosto com sabonete neutro antes do procedimento</li>
                                <li>🕐 Evite molhar os cílios por 24h após aplicação</li>
                                <li>🌙 Dormir de barriga para cima ajuda a preservar os fios</li>
                                <li>💧 Use apenas produtos oil-free na região dos olhos</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
