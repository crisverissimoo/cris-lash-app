import streamlit as st
import json, os
from datetime import datetime
hoje = datetime.now().date()

def txt(pt, es):  # Utilitário para texto bilíngue
    return pt if st.session_state.get("idioma") != "es" else es

# 🌸 Inicializa controle da tela
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = None
if "protocolo" not in st.session_state:
    st.session_state.protocolo = 1

# 🙋‍♀️ Área da Cliente
if st.session_state.pagina_atual == "cliente":
    escolha_cliente = st.radio("🧭 Como deseja acessar?", ["Já sou cliente", "Fazer novo cadastro"], index=None, key="opcao_cliente")

    # 🔐 Login Boutique com formulário
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

    # 🎀 Exibe histórico após login
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



    




# 🧾 Ficha Clínica — aparece se autorizada e cadastro confirmado
if st.session_state.get("cadastro_confirmado") and st.session_state.get("autorizada"):
    st.session_state.ficha_validada = st.session_state.get("ficha_validada", False)

    bloqueios = ["glaucoma", "infeccao", "conjuntivite", "cirurgia", "reacao"]
    alertas = ["alergia", "irritacao", "gravida", "acido", "sensibilidade"]
    informativos = ["colirio", "lentes", "extensao"]

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

                respostas = {}
                for chave, pergunta in perguntas.items():
                    col_p = st.columns([1, 4, 1])[1]
                    with col_p:
                        respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

                col_btn = st.columns([1, 2, 1])[1]
                with col_btn:
                    enviar = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar formulario"))

                if enviar:
                    if any(r is None for r in respostas.values()):
                        st.warning("⚠️ " + txt("Você precisa responder todas as perguntas antes de finalizar.",
                                                "Debe responder todas las preguntas antes de continuar."))
                        st.session_state.ficha_validada = False
                    else:
                        bloqueios_detectados = [f"- {perguntas[c]}" for c in bloqueios if respostas[c] == "Sim"]
                        alertas_detectados = [f"- {perguntas[c]}" for c in alertas if respostas[c] == "Sim"]
                        info_detectados = [f"- {perguntas[c]}" for c in informativos if respostas[c] == "Sim"]

                        if bloqueios_detectados:
                            st.error("❌ " + txt("Cliente não está apta para atendimento.", "Cliente no apta para atención") + "\n\n" + "\n".join(bloqueios_detectados))
                            st.session_state.ficha_validada = False
                            st.session_state.cliente_apta = False
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

      # 🧾 Ficha Clínica — aparece se autorizada e cadastro confirmado
if st.session_state.get("cadastro_confirmado") and st.session_state.get("autorizada"):
    st.session_state.ficha_validada = st.session_state.get("ficha_validada", False)

    bloqueios = ["glaucoma", "infeccao", "conjuntivite", "cirurgia", "reacao"]
    alertas = ["alergia", "irritacao", "gravida", "acido", "sensibilidade"]
    informativos = ["colirio", "lentes", "extensao"]

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

                respostas = {}
                for chave, pergunta in perguntas.items():
                    col_p = st.columns([1, 4, 1])[1]
                    with col_p:
                        respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

                col_btn = st.columns([1, 2, 1])[1]
                with col_btn:
                    enviar = st.form_submit_button(txt("📨 Finalizar ficha", "📨 Finalizar formulario"))

                if enviar:
                    if any(r is None for r in respostas.values()):
                        st.warning("⚠️ " + txt("Você precisa responder todas as perguntas antes de finalizar.",
                                                "Debe responder todas las preguntas antes de continuar."))
                        st.session_state.ficha_validada = False
                    else:
                        bloqueios_detectados = [f"- {perguntas[c]}" for c in bloqueios if respostas[c] == "Sim"]
                        alertas_detectados = [f"- {perguntas[c]}" for c in alertas if respostas[c] == "Sim"]
                        info_detectados = [f"- {perguntas[c]}" for c in informativos if respostas[c] == "Sim"]

                        if bloqueios_detectados:
                            st.error("❌ " + txt("Cliente não está apta para atendimento.", "Cliente no apta para atención") + "\n\n" + "\n".join(bloqueios_detectados))
                            st.session_state.ficha_validada = False
                            st.session_state.cliente_apta = False
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

# 🧵 Inicializa protocolo se necessário
if "protocolo" not in st.session_state:
    st.session_state.protocolo = 1

# 🎯 Etapa 3 — Escolha de data, horário e mensagem (liberada após escolher técnica)
if st.session_state.get("etapa_agendamento"):
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        with st.expander(txt("📅 Agendar Atendimento", "📅 Reservar cita"), expanded=True):
            st.markdown("<h4 style='text-align:center;'>📅 Agendar Atendimento</h4>", unsafe_allow_html=True)

            data_agendada = st.date_input(txt("Escolha a data do atendimento", "Elige la fecha de atención"), min_value=hoje)
            horarios_disponiveis = ["09:00", "11:00", "13:00", "15:00", "17:00"]
            horario_agendado = st.selectbox(txt("⏰ Horário disponível", "⏰ Horario disponible"), horarios_disponiveis)

            mensagem_cliente = st.text_area(txt("💬 Deseja deixar alguma observação?", "💬 ¿Desea dejar alguna observación?"))

            confirmar_agendamento = st.button(txt("✅ Confirmar agendamento", "✅ Confirmar cita"))

            if confirmar_agendamento and data_agendada and horario_agendado:
                novo_atendimento = {
                    "protocolo": f"{st.session_state.protocolo:05d}",
                    "nome": st.session_state.nome_cliente,
                    "telefone": st.session_state.telefone,
                    "tipo": st.session_state.efeito_escolhido,
                    "valor": st.session_state.tipo_aplicacao,
                    "data": str(data_agendada),
                    "horario": horario_agendado,
                    "mensagem": mensagem_cliente,
                }

                caminho = "agenda.json"
                historico = []
                if os.path.exists(caminho):
                    with open(caminho, "r", encoding="utf-8") as f:
                        historico = json.load(f)

                historico.append(novo_atendimento)

                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(historico, f, ensure_ascii=False, indent=2)

                st.session_state.protocolo += 1
                st.success(txt(
                    f"✅ Atendimento agendado com sucesso! Protocolo {novo_atendimento['protocolo']}",
                    f"✅ Cita confirmada correctamente. Protocolo {novo_atendimento['protocolo']}"
                ))

                # Limpa etapa para impedir reagendamento imediato
                st.session_state.etapa_agendamento = False


                
        # 5️⃣ Agendamento boutique — aparece se ficha validada
if st.session_state.get("ficha_validada"):
    st.markdown("""
        <div style='
            background-color: #f8d1d0;
            padding: 24px;
            border-radius: 12px;
            max-width: 520px;
            margin: auto;
            margin-top: 20px;
            text-align: center;
            border: 2px solid #cc4c73;
            color: #660000;
        '>
            <h4>📅 Agendamento Boutique</h4>
            <p style='font-size:14px;'>Agora escolha os detalhes do seu atendimento 💖</p>
        </div>
    """, unsafe_allow_html=True)

    efeito = st.selectbox("✨ Efeito desejado", ["Clássico", "Volume", "Híbrido"], key="efeito_ag")
    tecnica = st.selectbox("🎀 Técnica", ["Fio a fio", "Volume russo", "Mega volume"], key="tecnica_ag")
    valor = st.text_input("💲 Valor combinado", key="valor_ag")
    data = st.date_input("📅 Data do atendimento")
    horario = st.time_input("⏰ Horário do atendimento")
    mensagem = st.text_area("💬 Observação (opcional)", key="msg_ag")

    protocolo = f"CL{st.session_state.protocolo:04}"
    if st.button("📌 Finalizar agendamento"):
        cliente = {
            "protocolo": protocolo,
            "nome": st.session_state.nome_cliente,
            "telefone": st.session_state.telefone,
            "nascimento": str(st.session_state.nascimento),
            "email": st.session_state.email,
            "idade": st.session_state.idade_cliente,
            "efeito": efeito,
            "tipo": tecnica,
            "valor": valor,
            "data": str(data),
            "horario": str(horario),
            "mensagem": mensagem
        }

        caminho = "agenda.json"
        lista = []
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                lista = json.load(f)

        lista.append(cliente)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=2)

        st.session_state.protocolo += 1
        st.success(f"""
            💖 Atendimento agendado com sucesso!
            <br>🔢 Protocolo: <code>{protocolo}</code>
            <br>Obrigada por confiar na Cris Lash 👑
        """, unsafe_allow_html=True)


# 1️⃣ Botão de reprogramação — aparece se cliente logada e apta
if st.session_state.get("cliente_logada") and st.session_state.get("cliente_apta"):
    st.markdown("### 🗓️ Seus atendimentos anteriores")
    nome = st.session_state.nome_cliente
    tel = st.session_state.telefone

    caminho = "agenda.json"
    historico = []
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            historico = json.load(f)

    atendimentos = [c for c in historico if c.get("nome") == nome and c.get("telefone") == tel]

    for idx, cliente in enumerate(atendimentos):
        with st.expander(f"📌 Atendimento {idx+1} — protocolo {cliente['protocolo']}"):
            st.markdown(f"""
                <strong>🎀 Técnica:</strong> {cliente['tipo']} — {cliente['valor']}<br>
                <strong>📅 Data:</strong> {cliente['data']}<br>
                <strong>⏰ Horário:</strong> {cliente['horario']}<br>
                <strong>💬 Mensagem:</strong> {cliente['mensagem'] or '—'}
            """, unsafe_allow_html=True)

    # Botão para iniciar reprogramação
    if st.button("🔁 Reprogramar atendimento"):
        st.session_state.reprogramar = True
        st.session_state.atendimento_reprogramado = atendimentos[-1]  # usa o último como base
        st.experimental_rerun()

# 2️⃣ Se cliente deseja reprogramar
if st.session_state.get("reprogramar") and st.session_state.get("atendimento_reprogramado"):
    atendimento = st.session_state.atendimento_reprogramado

    with st.form("form_reprogramar"):
        st.markdown("### 🔁 Reprogramar Atendimento")

        novo_efeito = st.selectbox("✨ Escolha o novo efeito desejado", ["Volume Russo", "Fio a Fio", "Híbrido", "Leque 4D", "Colorido"])
        nova_tecnica = st.selectbox("🎀 Técnica", ["Clássica", "Avançada", "Express"])
        nova_data = st.date_input("📅 Nova data")
        novo_horario = st.selectbox("⏰ Horário", ["09:00", "11:00", "13:00", "15:00", "17:00"])
        nova_mensagem = st.text_area("💬 Mensagem ou observação (opcional)")

        confirmar = st.form_submit_button("✅ Confirmar reprogramação")

        if confirmar:
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






    
# 👑 Página Administrativa
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























# Bloco de agendamento
from datetime import datetime, timedelta
import os
import json

# Inicializa variável de controle se ainda não existe
if "etapa_agendamento" not in st.session_state:
    st.session_state.etapa_agendamento = False



# Bloco de agendamento
from datetime import datetime, timedelta
import os
import json

if st.session_state.get("efeito_escolhido") and st.session_state.get("tipo_aplicacao") and st.session_state.etapa_agendamento:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.expander("📅 Agendamento do Atendimento", expanded=True):
            data = st.date_input("📅 Escolha a data do atendimento", min_value=datetime.today().date())

            horarios_livres = [h for h in gerar_horarios() if esta_livre(data, h)]

            if not horarios_livres:
                st.warning("⛔ Nenhum horário disponível neste dia.")
            else:
                horario = st.selectbox("🕐 Escolha o horário", horarios_livres)
                fim = (datetime.strptime(horario, "%H:%M") + timedelta(hours=2)).strftime("%H:%M")

                nome = st.session_state.get("nome_cliente", "—")
                efeito = st.session_state.get("efeito_escolhido", "—")
                tipo = st.session_state.get("tipo_aplicacao", "—")
                valor = st.session_state.get("valor", "—")
                mensagem = st.text_area("📩 Mensagem adicional (opcional)", placeholder="Ex: alergia, dúvidas...")

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

                    # 🌸 Botão boutique de WhatsApp
                    numero_whatsapp = "34653841126"
                    mensagem_whatsapp = f"""
Olá, Cris! Sou {nome}, confirmando meu atendimento 💖

Protocolo: {protocolo}
Técnica: {tipo} — {efeito}
Dia: {data.strftime('%d/%m/%Y')} às {horario}
""".strip()

                    link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensagem_whatsapp.replace(' ', '%20').replace('\\n', '%0A')}"

                    st.markdown(f"""
                        <a href="{link_whatsapp}" target="_blank">
                            <button style="background-color:#f8d1d0; color:#660000; padding:10px 20px; border:none; border-radius:8px; font-weight:bold; margin-top:10px; margin-bottom:20px;">
                                📲 Enviar confirmação via WhatsApp
                            </button>
                        </a>
                    """, unsafe_allow_html=True)

                    # 💖 Cuidados pós-atendimento
                    st.markdown("""
                        <div style='background-color:#f8d1d0; padding:20px; border-radius:12px;'>
                            <h4 style='color:#660000;'>📌 Cuidados antes e depois da aplicação</h4>
                            <ul style='line-height:1.8; font-size:16px; color:#333333;'>
                                <li>🚫 Compareça sem maquiagem nos olhos</li>
                                <li>🧼 Lave o rosto com sabonete neutro antes do procedimento</li>
                                <li>🕐 Evite molhar os cílios por 24h após aplicação</li>
                                <li>🌙 Dormir de barriga para cima ajuda a preservar os fios</li>
                                <li>💧 Use apenas produtos oil-free na região dos olhos</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)


if st.session_state.get("agendamento_confirmado") and st.session_state.historico_clientes:
    ultimo = st.session_state.historico_clientes[-1]
    protocolo = ultimo.get("protocolo", "—")
    data_atend = ultimo.get("data", "—")
    horario_atend = ultimo.get("horario", "—")

    st.markdown("""
        <div class="painel-agradecimento">
            ✨ Atendimento confirmado com sucesso!<br><br>
            Protocolo nº <strong>{protocolo}</strong><br>
            Para <strong>{data_atend}</strong> às <strong>{horario_atend}</strong><br><br>
            💖 Obrigada por confiar na <em>Cris Lash</em><br>
            Cuide dos seus cílios com carinho — nos vemos em breve! 💐<br><br>
            <a href="/" target="_self">
                <button>🔁 Iniciar novo atendimento</button>
            </a>
        </div>
    """.format(protocolo=protocolo, data_atend=data_atend, horario_atend=horario_atend), unsafe_allow_html=True)


