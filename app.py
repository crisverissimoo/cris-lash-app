with st.expander("🗂️ Cadastro da Cliente"):
    nome_cliente = st.text_input("🧍 Nome completo", key="nome_cliente")
    nascimento = st.date_input(
        "📅 Data de nascimento",
        min_value=datetime(1920, 1, 1).date(),
        max_value=hoje,
        key="nascimento"
    )
    telefone = st.text_input("📞 Telefone", key="telefone")
    email = st.text_input("📧 Email (opcional)", key="email")

    # 🧠 Cálculo de idade
    idade = hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )
    menor = idade < 18
    st.write(f"📌 Idade: **{idade} anos**")

    if menor:
        responsavel = st.text_input("👨‍👩‍👧 Nome do responsável", key="responsavel")
        autorizacao = st.radio("Autorização recebida?", ["Sim", "Não", "Pendente"], index=None, key="aut_menor")
        if autorizacao != "Sim":
            st.error("❌ Cliente menor sem autorização — atendimento bloqueado.")
        autorizada = autorizacao == "Sim"
    else:
        autorizada = True  # Maior de idade, liberação automática

    if nascimento.month == hoje.month and nome_cliente:
        st.success(f"🎉 Parabéns, {nome_cliente}! Este mês é seu aniversário — a Cris Lash deseja ainda mais beleza e carinho! 💝")
