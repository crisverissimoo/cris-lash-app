import streamlit as st
from PIL import Image
from datetime import datetime
import pytz

# 🌍 Fuso horário local
fuso_espanha = pytz.timezone("Europe/Madrid")
agora_local = datetime.now(fuso_espanha)
hoje = agora_local.date()

# 🎨 Configuração da página
st.set_page_config(page_title="Consultoria Cris Lash", layout="wide")

# 🔐 Estado da sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "formato_escolhido" not in st.session_state:
    st.session_state.formato_escolhido = None
if "ficha_respostas" not in st.session_state:
    st.session_state.ficha_respostas = {}
if "ficha_validada" not in st.session_state:
    st.session_state.ficha_validada = False

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 💎 Sistema de Atendimento — Cris Lash")
    st.write(f"📅 Hoje é `{hoje.strftime('%d/%m/%Y')}`")

    # 🗂️ Cadastro
    with st.expander("🗂️ Cadastro da Cliente"):
        nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
        nascimento = st.date_input("📅 Data de nascimento", min_value=datetime(1920, 1, 1).date(), max_value=hoje, key="nascimento")
        telefone = st.text_input("📞 Telefone", key="telefone")
        email = st.text_input("📧 Email (opcional)", key="email")

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        menor = idade < 18
        st.write(f"📌 Idade: **{idade} anos**")

        if menor:
            responsavel = st.text_input("👨‍👩‍👧 Nome do responsável", key="responsavel")
            autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
            if autorizacao != "Sim":
                st.error("❌ Cliente menor sem autorização — atendimento bloqueado.")
            autorizada = autorizacao == "Sim"
        else:
            autorizada = True

        if nascimento.month == hoje.month and nome_cliente:
            st.success(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza e carinho! 💝")

  # 🧾 Ficha Clínica
    if autorizada:
        with st.expander("🧾 Ficha de Anamnese Clínica"):
            with st.form("ficha_anamnese"):
                perguntas = {
                    "lentes": "Usa lentes de contato?",
                    "alergia": "Tem histórico de alergias nos olhos ou pálpebras?",
                    "conjuntivite": "Já teve conjuntivite nos últimos 30 dias?",
                    "irritacao": "Está com olhos irritados ou lacrimejando frequentemente?",
                    "gravida": "Está grávida ou amamentando?",
                    "colirio": "Faz uso de colírios com frequência?",
                    "infeccao": "Tem blefarite, terçol ou outras infecções oculares?",
                    "cirurgia": "Fez cirurgia ocular recentemente?",
                    "acido": "Está em tratamento dermatológico com ácido?",
                    "sensibilidade": "Tem sensibilidade a produtos químicos ou cosméticos?",
                    "extensao": "Já fez extensão de cílios antes?",
                    "reacao": "Teve alguma reação alérgica em procedimentos anteriores?",
                    "glaucoma": "Possui glaucoma ou outra condição ocular diagnosticada?"
                }

                respostas = {}
                for chave, pergunta in perguntas.items():
                    respostas[chave] = st.radio(pergunta, ["Sim", "Não"], index=None, key=f"clinica_{chave}")

                enviar_ficha = st.form_submit_button("📨 Finalizar ficha")

                if enviar_ficha:
                    if None in respostas.values():
                        st.error("⚠️ Responda todas as perguntas.")
                        st.session_state.ficha_validada = False
                    else:
                        bloqueios_criticos = []
                        if respostas["infeccao"] == "Sim": bloqueios_criticos.append("Infecção ocular ativa")
                        if respostas["conjuntivite"] == "Sim": bloqueios_criticos.append("Conjuntivite recente")
                        if respostas["cirurgia"] == "Sim": bloqueios_criticos.append("Cirurgia ocular recente")
                        if respostas["reacao"] == "Sim": bloqueios_criticos.append("Reação alérgica anterior")
                        if respostas["glaucoma"] == "Sim": bloqueios_criticos.append("Glaucoma")

                        if respostas["gravida"] == "Sim":
                            st.warning("⚠️ Gestante ou lactante — recomenda-se autorização médica.")
                        if respostas["glaucoma"] == "Sim" or respostas["cirurgia"] == "Sim":
                            st.warning("⚠️ Liberação médica obrigatória.")

                        if bloqueios_criticos:
                            st.warning("⚠️ Cliente com condições que impedem o procedimento:")
                            for item in bloqueios_criticos:
                                st.markdown(f"- {item}")
                            st.error("❌ Atendimento não permitido neste momento. Agende nova data após liberação médica.")
                            st.session_state.ficha_validada = False
                        else:
                            st.success("✅ Cliente apta para atendimento!")
                            st.session_state.ficha_validada = True

                        # 👁️ Identificação do Formato de Olho — só com botões
        with st.expander("👁️ Identifique o formato do seu olhar"):
            st.write("Veja abaixo os estilos e clique no que mais se parece com o seu:")

            formatos = {
                "Olhos Caídos": {
                    "imagem": "URL_OLHO_CAIDO",
                    "sugestao": "Volume russo — realça e corrige o caimento"
                },
                "Olhos Pequenos": {
                    "imagem": "URL_OLHO_PEQUENO",
                    "sugestao": "Fio a fio ou Híbrido — leve e alonga com delicadeza"
                },
                "Olhos Grandes": {
                    "imagem": "URL_OLHO_GRANDE",
                    "sugestao": "Híbrido — suaviza e valoriza o contorno"
                },
                "Olhos Asiáticos": {
                    "imagem": "URL_OLHO_ASIATICO",
                    "sugestao": "Híbrido — define sem pesar"
                },
                "Pálpebra Caída": {
                    "imagem": "URL_PALPEBRA_CAIDA",
                    "sugestao": "Fio a fio — leve e natural"
                },
                "Olhos Juntos": {
                    "imagem": "URL_OLHO_JUNTO",
                    "sugestao": "Fio a fio — evita efeito fechado e alonga sutilmente"
                },
                "Olhos Separados": {
                    "imagem": "URL_OLHO_SEPARADO",
                    "sugestao": "Volume russo — dá destaque ao centro e equilibra distância"
                },
                "Olhos Padrão": {
                    "imagem": "URL_OLHO_PADRAO",
                    "sugestao": "Qualquer técnica — aceita bem todas"
                }
            }

            colunas = st.columns(2)
            index = 0
            for tipo, dados in formatos.items():
                with colunas[index % 2]:
                    st.image(dados["imagem"], caption=f"{tipo}", use_column_width=True)
                    if st.button(f"✅ Esse se parece comigo", key=f"botao_{tipo}"):
                        st.session_state.tipo_olho = tipo
                        st.session_state.sugestao_tecnica = dados["sugestao"]
                        st.success(f"👁️ Formato selecionado: **{tipo}**")
                        st.info(f"💡 Sugestão de técnica: **{dados['sugestao']}**")
                index += 1

    
        # 👁️ Tipo de Olho + Sugestão de Técnica
        with st.expander("👁️ Tipo de Olho da Cliente"):
            tipo_olho = st.selectbox("Qual o formato predominante dos olhos da cliente?", [
                "Padrão",
                "Pequeno",
                "Caído",
                "Asiático",
                "Abertos",
                "Arredondado",
                "Profundo",
                "Pálpebra caída",
                "Outro"
            ], key="tipo_olho")

            sugestao = ""
            if tipo_olho == "Caído":
                sugestao = "Volume russo — realça o olhar e corrige o caimento"
            elif tipo_olho == "Pequeno":
                sugestao = "Fio a fio ou Híbrido — evita sobrecarga visual e alonga com leveza"
            elif tipo_olho == "Asiático":
                sugestao = "Híbrido — preenche com definição sem pesar"
            elif tipo_olho == "Abertos":
                sugestao = "Híbrido ou Colorido — destaca o formato e permite brincar com cor"
            elif tipo_olho == "Profundo":
                sugestao = "Volume russo ou Híbrido — ajuda a trazer profundidade e destaque"
            elif tipo_olho == "Pálpebra caída":
                sugestao = "Fio a fio — natural, leve e adequado para não pesar o olhar"
            elif tipo_olho == "Arredondado":
                sugestao = "Híbrido — suaviza e valoriza o contorno"
            elif tipo_olho == "Padrão":
                sugestao = "Qualquer técnica — o formato aceita bem todas as abordagens"

            if sugestao:
                st.success(f"👁️ Sugestão: **{sugestao}**")

    # 🎨 Escolha de Técnica
    if st.session_state.ficha_validada:
        with st.expander("🎨 Escolha da Técnica"):
            st.write("Selecione a técnica desejada para este atendimento:")

            formatos = {
                "Fio a fio": "✨ Natural, delicado e clássico",
                "Volume russo": "💥 Impactante, curvado e volumoso",
                "Híbrido": "⚖️ Equilíbrio entre clássico e volume",
                "Colorido": "🌈 Criativo e com tons vibrantes"
            }

            for nome, descricao in formatos.items():
                if st.button(nome, key=f"formato_{nome}"):
                    st.session_state.formato_escolhido = nome
                    st.success(f"Técnica selecionada: **{nome}** — {descricao}")


                # 📸 Foto da Cliente
        with st.expander("📸 Foto da Cliente"):
            tipo_imagem = st.radio("Como deseja adicionar a imagem?", ["Upload", "Câmera"], index=0, key="tipo_imagem")
            if tipo_imagem == "Upload":
                imagem_cliente = st.file_uploader("📎 Enviar imagem", type=["jpg", "jpeg", "png"], key="upload_foto")
            else:
                imagem_cliente = st.camera_input("📷 Tirar foto agora", key="camera_foto")

            if imagem_cliente:
                st.image(imagem_cliente, caption="📸 Prévia da imagem enviada", use_column_width=True)

        # 📝 Observações
        with st.expander("📝 Observações Personalizadas"):
            observacoes = st.text_area("Comentários sobre o atendimento, preferências, cuidados especiais…", key="obs_cliente")

        # ⏰ Agendamento
        with st.expander("⏰ Agendamento"):
            horarios_disponiveis = ["09:00", "10:30", "12:00", "14:00", "15:30", "17:00"]
            horario_escolhido = st.selectbox("Selecione o horário disponível:", horarios_disponiveis, key="horario_agendamento")
            if horario_escolhido:
                st.success(f"🗓️ Atendimento agendado para `{horario_escolhido}`.")

        # 🗂️ Histórico do Atendimento
        with st.expander("🗂️ Histórico da Cliente"):
            if st.button("📌 Registrar Atendimento", key="registrar_atend"):
                registro = {
                    "nome": st.session_state.nome_cliente,
                    "idade": idade,
                    "tipo_olho": st.session_state.get("tipo_olho", "Não informado"),
                    "sugestao_tecnica": st.session_state.get("sugestao_tecnica", "Não gerada"),
                    "tecnica_escolhida": st.session_state.get("formato_escolhido", "Não selecionada"),
                    "observacoes": st.session_state.get("obs_cliente", ""),
                    "horario": st.session_state.get("horario_agendamento", "Não agendado"),
                    "data": hoje.strftime("%d/%m/%Y")
                }
                st.session_state.historico.append(registro)
                st.success("✅ Atendimento registrado com sucesso!")

            # 📋 Exibir registros salvos
            if st.session_state.historico:
                for i, atend in enumerate(st.session_state.historico[::-1]):
                    st.markdown(f"### 🧍 Atendimento #{len(st.session_state.historico)-i}")
                    st.write(f"📅 Data: `{atend['data']} — {atend['horario']}`")
                    st.write(f"👁️ Tipo de olho: **{atend['tipo_olho']}**")
                    st.write(f"💡 Sugestão de técnica: *{atend['sugestao_tecnica']}*")
                    st.write(f"🎨 Técnica escolhida: **{atend['tecnica_escolhida']}**")
                    if atend["observacoes"]:
                        st.markdown(f"📝 Observações: {atend['observacoes']}")
                    st.markdown("---")
            else:
                st.info("ℹ️ Nenhum atendimento registrado ainda.")

