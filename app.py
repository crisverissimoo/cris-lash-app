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

      # ✨ Estilos Visuais + Indicação
with st.expander("✨ Estilos Visuais + Indicação"):
    st.markdown("""
    ## 🌿 Clássico  
    🖼️ [Imagem do estilo Clássico]  
    🔘 **Clássico**  
    📌 Indicado para todos os tipos de olhos  
    ✨ Efeito leve, natural e equilibrado — ideal para iniciantes ou quem busca discrição

    ---

    ## 🧸 Boneca  
    🖼️ [Imagem do estilo Boneca]  
    🔘 **Boneca**  
    📌 Indicado para olhos pequenos, amendoados ou asiáticos  
    ✨ Efeito aberto e arredondado como o de uma boneca

    ---

    ## 🐱 Gatinho  
    🖼️ [Imagem do estilo Gatinho]  
    🔘 **Gatinho**  
    📌 Indicado para olhos juntos, saltados ou amendoados  
    ✨ Efeito puxado, felino e sofisticado

    ---

    ## 🐿️ Esquilo  
    🖼️ [Imagem do estilo Esquilo]  
    🔘 **Esquilo**  
    📌 Indicado para olhos caídos, encapotados ou amendoados  
    ✨ Efeito elevado e elegante que levanta o olhar sem exagero
    """)

# 📝 Observações Personalizadas
with st.expander("📝 Observações Personalizadas"):
    st.text_area("Anotações do atendimento", key="observacoes_cliente")

# 📅 Agendamento
with st.expander("📅 Agendamento"):
    st.date_input("Data do atendimento", key="data_atendimento")
    st.time_input("Horário do atendimento", key="horario_atendimento")

# 📚 Histórico da Cliente
with st.expander("📚 Histórico da Cliente"):
    st.text_area("Últimos atendimentos ou observações relevantes", key="historico_cliente")

# 🧾 Registro da Sessão
registro = {
    "Tipo de olho": st.session_state.get("tipo_olho", ""),
    "Técnica sugerida": st.session_state.get("sugestao_tecnica", ""),
    "Técnica escolhida": st.session_state.get("formato_escolhido", ""),
    "Data": st.session_state.get("data_atendimento", ""),
    "Horário": st.session_state.get("horario_atendimento", ""),
    "Histórico": st.session_state.get("historico_cliente", ""),
    "Observações": st.session_state.get("observacoes_cliente", "")
}

# Salvar registro
