import streamlit as st

st.title("💰 Finix IA")
st.write("Assistente de planejamento financeiro inteligente")

# Funções
def calcular_juros_compostos(valor, taxa, tempo):
    return valor * (1 + taxa) ** tempo

# Menu
opcao = st.selectbox("Escolha uma função:", [
    "Planejamento Financeiro",
    "Calcular Investimento",
    "Dicas para enriquecer",
    "Controle de gastos",
    "Renda extra"
])

# Planejamento financeiro
if opcao == "Planejamento Financeiro":
    salario = st.number_input("Renda mensal (R$)", min_value=0.0)
    gastos = st.number_input("Gastos mensais (R$)", min_value=0.0)

    if st.button("Calcular"):
        sobra = salario - gastos

        if sobra <= 0:
            st.error("Você está gastando mais do que ganha.")
        else:
            investimento = sobra * 0.5
            reserva = sobra * 0.3
            lazer = sobra * 0.2

            st.success(f"Sobra: R$ {sobra:.2f}")
            st.write(f"Investimentos: R$ {investimento:.2f}")
            st.write(f"Reserva: R$ {reserva:.2f}")
            st.write(f"Lazer: R$ {lazer:.2f}")

# Investimento
elif opcao == "Calcular Investimento":
    valor = st.number_input("Valor inicial (R$)", min_value=0.0)
    taxa = st.number_input("Taxa anual (%)", min_value=0.0)
    tempo = st.number_input("Tempo (anos)", min_value=1)

    if st.button("Simular"):
        montante = calcular_juros_compostos(valor, taxa/100, tempo)
        st.success(f"Montante final: R$ {montante:.2f}")

# Dicas
elif opcao == "Dicas para enriquecer":
    st.write("""
    - Aumente sua renda
    - Invista com consistência
    - Tenha disciplina e paciência
    """)

elif opcao == "Controle de gastos":
    st.write("""
    - Registre gastos por 30 dias
    - Corte excessos
    - Priorize investimentos
    """)

elif opcao == "Renda extra":
    st.write("""
    - Freelance
    - Revenda
    - Criar conteúdo
    """)
