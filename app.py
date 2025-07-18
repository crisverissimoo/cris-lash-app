import streamlit as st
import json, os
from datetime import datetime
hoje = datetime.now().date()

def txt(pt, es):
    return pt if st.session_state.get("idioma") != "es" else es

# Inicializa variáveis boutique
for chave in [
    "pagina_atual", "cliente_logada", "cadastro_confirmado", "ficha_validada", "cliente_apta",
    "protocolo", "autorizada", "efeito_escolhido", "tipo_aplicacao", "etapa_agendamento",
    "historico_cliente", "reprogramar", "atendimento_reprogramado", "valor"
]:
    if chave not in st.session_state:
        st.session_state[chave] = None if chave != "protocolo" else 1

# Área da cliente
if st.session_state.pagina_atual == "cliente":

    escolha_cliente = st.radio("🧭 Como deseja acessar?", ["Já sou cliente", "Fazer novo cadastro"], index=None, key="opcao_cliente")

    if escolha_cliente == "Já sou cliente":
        with st.form("form_login_cliente"):
            nome_login = st.text_input("🧍 Seu nome")
            tel_login = st.text_input("📱 Seu telefone com DDD")
            confirmar_login = st.form_submit_button("✅ Entrar")

            if confirmar_login and nome_login and tel_login:
                caminho = "agenda.json"
                historico = []
                if os.path.exists(caminho):
                    with open(caminho, "r", encoding="utf-8") as f:
                        historico = json.load(f)

                atendimentos = [c for c in historico if c.get("nome") == nome_login and c.get("telefone") == tel_login]

                if atendimentos:
                    st.session_state.cliente_logada = True
                    st.session_state.nome_cliente = nome_login
                    st.session_state.telefone = tel_login
                    st.session_state.historico_cliente = atendimentos
                    st.success("✨ Login confirmado com sucesso! Bem-vinda de volta 💖")
                    st.experimental_rerun()
                else:
                    st.warning("🙈 Não encontramos seus dados. Verifique o nome e telefone.")

    elif escolha_cliente == "Fazer novo cadastro":
        with st.form("form_cadastro"):
            nome = st.text_input("🧍 Nome completo")
            nascimento = st.date_input("📅 Data de nascimento", min_value=datetime(1920, 1, 1).date(), max_value=hoje)
            telefone = st.text_input("📞 Telefone com DDD")
            email = st.text_input("📧 Email (opcional)")

            idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
            menor = idade < 18

            st.session_state.autorizada = True
            st.info(f"📌 Idade: **{idade} anos**")

            if menor:
                responsavel = st.text_input("👨‍👩‍👧 Nome do responsável")
                autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None)
                if autorizacao != "Sim":
                    st.error("❌ Cliente menor sem autorização — atendimento bloqueado.")
                    st.session_state.autorizada = False

            confirmar = st.form_submit_button("✅ Confirmar cadastro")

            if confirmar:
                campos_ok = nome and telefone and nascimento and idade >= 0
                if menor:
                    campos_ok = campos_ok and st.session_state.autorizada

                if campos_ok:
                    st.session_state.nome_cliente = nome
                    st.session_state.nascimento = nascimento
                    st.session_state.telefone = telefone
                    st.session_state.email = email
                    st.session_state.idade_cliente = idade
                    st.session_state.cadastro_confirmado = True
                    st.success("✅ Cadastro finalizado com sucesso!")
                    st.experimental_rerun()
                else:
                    st.warning("⚠️ Preencha todos os dados corretamente para continuar.")


    # 🧾 Ficha Clínica — aparece após cadastro confirmado e cliente autorizada
    if st.session_state.get("cadastro_confirmado") and st.session_state.get("autorizada"):
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


    # ✨ Escolha de Efeito Lash
    if st.session_state.ficha_validada and st.session_state.cliente_apta:
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
                    col_img, col_txt = st.columns([1.8, 1.2])
                    with col_img:
                        st.image(efeito["img"], width=500)
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
                    st.success("✅ " + txt(f"Efeito selecionado: {nome}", f"Efecto seleccionado: {nome}"))

    # 🎀 Escolha da Técnica
    if st.session_state.get("efeito_escolhido") and not st.session_state.etapa_agendamento:
        if "etapa_agendamento" not in st.session_state:
            st.session_state.etapa_agendamento = False

        col_esq, col_centro, col_dir = st.columns([1, 2, 1])
        with col_centro:
            with st.expander(txt("🎀 Tipo de Aplicação", "🎀 Técnica de aplicación"), expanded=True):
                st.markdown("<h4 style='text-align:center;'>🎀 Técnica de Aplicação</h4>", unsafe_allow_html=True)

                tipos = {
                    "Egípcio 3D": {
                        "img": "https://i.imgur.com/TOPRWFQ.jpeg",
                        "desc": txt("Leque 3D artístico — acabamento definido e sofisticado.", "Abanico 3D artístico — acabado definido y sofisticado."),
                        "valor": "25€"
                    },
                    "Volume Russo 4D": {
                        "img": "https://i.imgur.com/tBX2O8e.jpeg",
                        "desc": txt("4 fios por cílio — volume intenso e estruturado.", "4 fibras por pestaña — volumen intenso y estructurado."),
                        "valor": "25€"
                    },
                    "Volume Brasileiro": {
                        "img": "https://i.imgur.com/11rw6Jv.jpeg",
                        "desc": txt("Formato Y — volumoso e natural.", "Formato Y — voluminoso y natural."),
                        "valor": "25€"
                    },
                    "Fio a Fio": {
                        "img": "https://i.imgur.com/VzlySv4.jpeg",
                        "desc": txt("1 fio por cílio — efeito rímel natural.", "1 fibra por pestaña — efecto natural tipo máscara."),
                        "valor": "25€"
                    }
                }

                for i, (nome, tipo) in enumerate(tipos.items()):
                    st.markdown("<hr style='margin-top:30px; margin-bottom:30px;'>", unsafe_allow_html=True)
                    col_img, col_txt = st.columns([1.6, 1.4])
                    with col_img:
                        st.markdown(f"<div style='text-align:center;'><img src='{tipo['img']}' alt='{nome}' style='width:220px; border-radius:8px;'></div>", unsafe_allow_html=True)
                    with col_txt:
                        st.markdown(f"<h5 style='text-align:center;'>{nome} — 💶 {tipo['valor']}</h5>", unsafe_allow_html=True)
                        st.caption(tipo["desc"])
                        col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
                        with col_b2:
                            if st.button(txt(f"Selecionar {nome}", f"Seleccionar {nome}"), key=f"tipo_{nome}_{i}"):
                                st.session_state.tipo_aplicacao = nome
                                st.session_state.valor = tipo["valor"]
                                st.session_state.etapa_agendamento = True

                if st.session_state.get("tipo_aplicacao"):
                    selecionado = st.session_state.tipo_aplicacao
                    st.success(txt(f"✅ Tipo selecionado: {selecionado} — 💶 {tipos[selecionado]['valor']}", f"✅ Técnica seleccionada: {selecionado} — 💶 {tipos[selecionado]['valor']}"))

    # 📅 Agendamento Boutique
    if st.session_state.get("etapa_agendamento"):
        with st.form("form_agendamento"):
            st.markdown("### 📅 Agendamento")
            data = st.date_input("📆 Escolha a data")
            horario = st.selectbox("⏰ Horário disponível", ["09:00", "11:00", "13:00", "15:00", "17:00"])
            obs = st.text_area("💬 Observação (opcional)")
            confirmar = st.form_submit_button("✅ Confirmar Agendamento")

            if confirmar:
                protocolo = st.session_state.protocolo
                novo = {
                    "protocolo": protocolo,
                    "nome": st.session_state.nome_cliente,
                    "telefone": st.session_state.telefone,
                    "tipo": st.session_state.efeito_escolhido,
                    "valor": st.session_state.tipo_aplicacao + " — " + st.session_state.valor,
                    "data": str(data),
                    "horario": horario,
                    "mensagem": obs
                }

                caminho = "agenda.json"
                historico = []
                if os.path.exists(caminho):
                    with open(caminho, "r", encoding="utf-8") as f:
                        historico = json.load(f)

                historico.append(novo)

                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(historico, f, indent=2, ensure_ascii=False)

                st.session_state.protocolo += 1
                st.success("✅ Agendamento confirmado com sucesso!")
                st.balloons()


    # 💼 Histórico boutique
    if st.session_state.get("cliente_logada") and isinstance(st.session_state.get("historico_cliente"), list):
        st.markdown(f"### 💼 Histórico de {st.session_state.nome_cliente}")
        for idx, cliente in enumerate(st.session_state["historico_cliente"]):
            with st.expander(f"📌 Atendimento {idx + 1} — protocolo {cliente['protocolo']}"):
                st.markdown(f"""
                    <strong>🎀 Técnica:</strong> {cliente['tipo']} — {cliente['valor']}<br>
                    <strong>📅 Data:</strong> {cliente['data']}<br>
                    <strong>⏰ Horário:</strong> {cliente['horario']}<br>
                    <strong>💬 Mensagem:</strong> {cliente['mensagem'] or '—'}
                """, unsafe_allow_html=True)

    # 🔁 Reprogramar atendimento direto
    if st.session_state.get("cliente_logada") and st.session_state.get("cliente_apta"):
        if st.button("🔁 Reprogramar último atendimento"):
            atendimentos = st.session_state.historico_cliente
            st.session_state.reprogramar = True
            st.session_state.atendimento_reprogramado = atendimentos[-1]
            st.experimental_rerun()

    if st.session_state.get("reprogramar") and st.session_state.get("atendimento_reprogramado"):
        atendimento = st.session_state.atendimento_reprogramado
        with st.form("form_reprogramar"):
            st.markdown("### 🔁 Reprogramar Atendimento")

            novo_efeito = st.selectbox("✨ Novo efeito desejado", ["Clássica", "Boneca", "Gatinho", "Esquilo"])
            nova_tecnica = st.selectbox("🎀 Nova técnica", ["Egípcio 3D", "Volume Russo 4D", "Volume Brasileiro", "Fio a Fio"])
            nova_data = st.date_input("📅 Nova data")
            novo_horario = st.selectbox("⏰ Novo horário", ["09:00", "11:00", "13:00", "15:00", "17:00"])
            nova_mensagem = st.text_area("💬 Mensagem (opcional)")

            confirmar = st.form_submit_button("✅ Confirmar reprogramação")

            if confirmar:
                caminho = "agenda.json"
                historico = []
                if os.path.exists(caminho):
                    with open(caminho, "r", encoding="utf-8") as f:
                        historico = json.load(f)

                for cliente in historico:
                    if cliente["protocolo"] == atendimento["protocolo"]:
                        cliente["tipo"] = novo_efeito
                        cliente["valor"] = nova_tecnica
                        cliente["data"] = str(nova_data)
                        cliente["horario"] = novo_horario
                        cliente["mensagem"] = nova_mensagem
                        break

                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(historico, f, indent=2, ensure_ascii=False)

                st.success("✅ Atendimento reprogramado com sucesso!")
                st.session_state.reprogramar = False
                st.session_state.atendimento_reprogramado = None

    # ❌ Cancelar atendimento
    if st.session_state.get("cliente_logada") and isinstance(st.session_state.get("historico_cliente"), list):
        st.markdown("### ❌ Cancelar Atendimento")
        opcoes_cancelamento = [
            f"{c['data']} — {c['horario']} — protocolo {c['protocolo']}" for c in st.session_state.historico_cliente
        ]
        selecionado = st.selectbox("📍 Escolha atendimento para cancelar", opcoes_cancelamento, index=None)
        confirmar = st.button("⚠️ Cancelar atendimento")

        if confirmar and selecionado:
            protocolo_cancelar = int(selecionado.split("protocolo ")[-1])
            caminho = "agenda.json"
            historico = []
            if os.path.exists(caminho):
                with open(caminho, "r", encoding="utf-8") as f:
                    historico = json.load(f)
            historico = [c for c in historico if c["protocolo"] != protocolo_cancelar]
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(historico, f, indent=2, ensure_ascii=False)
            st.success("🚫 Atendimento cancelado com sucesso!")

    # 📤 Botão WhatsApp
    if st.session_state.get("cliente_logada") and st.session_state.get("historico_cliente"):
        ultimo = st.session_state.historico_cliente[-1]
        texto = f"""💖 Atendimento Boutique confirmado!

📍 Técnica: {ultimo['tipo']} — {ultimo['valor']}
📅 Data: {ultimo['data']} às {ultimo['horario']}
💬 Mensagem: {ultimo['mensagem'] or '—'}
📌 Protocolo: {ultimo['protocolo']}

Para dúvidas ou reagendamentos, fale conosco 🥰"""

        link = f"https://wa.me/?text={texto.replace(' ', '%20').replace('\n', '%0A')}"
        st.markdown(f"[📲 Enviar detalhes via WhatsApp]({link})", unsafe_allow_html=True)



# 👩‍💼 Área Administrativa
if st.session_state.pagina_atual == "admin":
    st.markdown("## 👩‍💼 Painel Administrativo")

    # Carrega agendamentos do JSON
    caminho = "agenda.json"
    lista_admin = []
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            lista_admin = json.load(f)

    if lista_admin:
        opcoes_admin = [f"{c['data']} — {c['horario']} — {c['nome']} — protocolo {c['protocolo']}" for c in lista_admin]
        atendimento_admin = st.selectbox("📋 Selecione atendimento:", opcoes_admin, index=None, key="admin_escolha")

        if atendimento_admin:
            idx = opcoes_admin.index(atendimento_admin)
            cliente = lista_admin[idx]

            st.markdown(f"#### 📌 Detalhes de protocolo `{cliente['protocolo']}`")
            st.write(cliente)

            col1, col2 = st.columns(2)

            with col1:
                confirmar_cancelar = st.button("❌ Cancelar Atendimento")
                if confirmar_cancelar:
                    lista_admin.pop(idx)
                    with open(caminho, "w", encoding="utf-8") as f:
                        json.dump(lista_admin, f, ensure_ascii=False, indent=2)
                    st.success("✅ Atendimento cancelado com sucesso!")

            with col2:
                import urllib.parse
                fone = cliente["telefone"].replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
                mensagem = f"""
✨ Atendimento confirmado na Cris Lash 👑
📌 Protocolo: {cliente['protocolo']}
📅 Data: {cliente['data']} às {cliente['horario']}
🎀 Técnica: {cliente.get('tipo', cliente.get('valor', ''))}
💬 Obs.: {cliente.get('mensagem', '—')}
"""
                link = f"https://wa.me/55{fone}?text={urllib.parse.quote(mensagem)}"
                st.markdown(f"[📤 Enviar via WhatsApp]({link})", unsafe_allow_html=True)
    else:
        st.warning("📭 Nenhum atendimento registrado ainda.")






elif st.session_state.pagina_atual == "adm":
    st.markdown("<h4>🔐 Área Administrativa</h4>", unsafe_allow_html=True)
    codigo = st.text_input("🔑 Código de acesso", type="password")
    if st.button("🔓 Entrar"):
        if codigo.strip().lower() == "rainha":
            st.session_state.acesso_admin = True
            st.success("💎 Acesso liberado!")
        else:
            st.error("❌ Código inválido.")

    if st.session_state.acesso_admin:
        st.markdown("""
            <div class='box'>
                <h4>👑 Painel Administrativo</h4>
                <p>Gerencie atendimentos com carinho 💖</p>
            </div>
        """, unsafe_allow_html=True)

        caminho_arquivo = "agenda.json"
        clientes_salvos = []
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                clientes_salvos = json.load(f)

        st.markdown("### 📋 Lista de atendimentos")
        if clientes_salvos:
            clientes_salvos.sort(key=lambda c: c["protocolo"])
            for idx, cliente in enumerate(clientes_salvos):
                with st.container():
                    st.markdown(f"""
                        <div style='background-color:#d495a2; padding:15px; border-radius:8px;'>
                            <strong>🔢 Protocolo:</strong> {cliente['protocolo']}<br>
                            <strong>🧍 Nome:</strong> {cliente['nome']}<br>
                            <strong>✨ Efeito:</strong> {cliente['efeito']}<br>
                            <strong>🎀 Técnica:</strong> {cliente['tipo']}{" — "}{cliente['valor']}<br>
                            <strong>📅 Data:</strong> {cliente['data']}<br>
                            <strong>⏰ Horário:</strong> {cliente['horario']}<br>
                            <strong>💬 Mensagem:</strong> {cliente['mensagem'] or '—'}
                        </div>
                    """, unsafe_allow_html=True)

                    if st.button(f"❌ Excluir {cliente['protocolo']}", key=f"excluir_{idx}"):
                        confirmar = st.radio(f"⚠️ Confirmar exclusão de {cliente['protocolo']}?", ["Cancelar", "Confirmar"], key=f"confirmar_{idx}")
                        if confirmar == "Confirmar":
                            clientes_salvos.pop(idx)
                            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                                json.dump(clientes_salvos, f, ensure_ascii=False, indent=2)
                            st.success("✅ Atendimento excluído!")
                            st.experimental_rerun()
        else:
            st.info("📂 Nenhum atendimento registrado.")


        # 📅 Horários ocupados
        st.markdown("### 📅 Horários ocupados")
        if st.session_state.historico_ocupados:
            agenda = {}
            for data, hora in st.session_state.historico_ocupados:
                dia_str = data.strftime('%d/%m/%Y')




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
                    
if st.session_state.get("agendamento_confirmado"):
    cliente = st.session_state.historico_clientes[-1]

    st.markdown(f"""
        <strong> Protocolo:</strong> {cliente['protocolo']}<br>
        <strong> Nome:</strong> {cliente['nome']}<br>
        <strong> Efeito:</strong> {cliente['efeito']}<br>
        <strong> Técnica:</strong> {cliente['tipo']} — 💶 {cliente['valor']}<br>
        <strong> Data:</strong> {cliente['data']} — 🕐 {cliente['horario']}<br>
        <strong> Observações:</strong> {cliente['mensagem'] or '—'}<br>
    """, unsafe_allow_html=True)



# 🧠 Estados iniciais
for key in ["ficha_validada", "cliente_apta", "efeito_escolhido", "tipo_aplicacao", "valor", "agendamento_confirmado", "cadastro_completo"]:
    if key not in st.session_state:
        st.session_state[key] = None
for key in ["historico_ocupados", "historico_clientes", "protocolo"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key != "protocolo" else 1
























