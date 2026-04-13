import streamlit as st
import time
import re
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Finix IA", page_icon="💰", layout="centered")

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #e5e7eb;
}
h1 {
    text-align: center;
}
section[data-testid="stSidebar"] {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<h1>💰 Finix IA</h1>
<p style='text-align:center; color: gray;'>
Assistente financeiro estratégico
</p>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (SIMULADOR REAL)
# =========================
with st.sidebar:
    st.header("📊 Simulador de Investimento")

    valor = st.number_input("Valor mensal (R$)", min_value=0.0, value=200.0)
    anos = st.slider("Tempo (anos)", 1, 30, 10)
    taxa = st.slider("Taxa (% ao ano)", 1, 20, 10)

    if st.button("Simular"):
        meses = anos * 12
        saldo = 0
        historico = []

        for _ in range(meses):
            saldo = saldo * (1 + taxa/100/12) + valor
            historico.append(saldo)

        st.success(f"Resultado final: R${saldo:,.2f}")

        # gráfico
        plt.figure()
        plt.plot(historico)
        plt.xlabel("Meses")
        plt.ylabel("Dinheiro")
        plt.title("Crescimento do investimento")
        st.pyplot(plt)

    st.divider()

    st.header("📌 Dados atuais")
    renda = st.session_state.get("renda", "—")
    gastos = st.session_state.get("gastos", "—")

    st.write(f"Renda: R${renda}")
    st.write(f"Gastos: R${gastos}")

    if st.button("Limpar tudo"):
        st.session_state.clear()
        st.rerun()

# =========================
# INTENÇÕES
# =========================
def detectar_intencoes(p):
    intents = {
        "saudacao": ["oi", "olá", "fala"],
        "planejamento": ["organizar", "planejamento", "finanças"],
        "investimento": ["investir", "juros", "investimento"],
        "gastos": ["gastos", "despesas"],
        "renda": ["renda extra", "ganhar dinheiro"],
        "riqueza": ["rico", "enriquecer"]
    }

    encontrados = []
    for intent, palavras in intents.items():
        for palavra in palavras:
            if palavra in p:
                encontrados.append(intent)
                break
    return encontrados

def extrair_numeros(p):
    numeros = re.findall(r'\d+', p)
    return [int(n) for n in numeros]

# =========================
# RESPOSTA
# =========================
def responder(pergunta):
    p = pergunta.lower()
    intencoes = detectar_intencoes(p)
    numeros = extrair_numeros(p)

    partes = []

    # SAUDAÇÃO
    if "saudacao" in intencoes:
        partes.append("Tudo sob controle. Vamos direto ao ponto.\n")

    # SALVAR DADOS
    if len(numeros) >= 2:
        st.session_state["renda"] = numeros[0]
        st.session_state["gastos"] = numeros[1]

    renda = st.session_state.get("renda")
    gastos = st.session_state.get("gastos")

    # PLANEJAMENTO
    if "planejamento" in intencoes:
        if renda is not None and gastos is not None:
            sobra = renda - gastos

            if sobra <= 0:
                partes.append(f"""
Você ganha R${renda} e gasta R${gastos}.

Está no negativo.

Ação:
- cortar gastos
- aumentar renda
""")
            else:
                partes.append(f"""
Renda: R${renda}
Gastos: R${gastos}
Sobra: R${sobra}

Distribuição:
- Investir: R${sobra*0.5:.0f}
- Reserva: R${sobra*0.3:.0f}
- Lazer: R${sobra*0.2:.0f}

Se mantiver isso, sua situação melhora rápido.
""")
        else:
            partes.append("Me diga sua renda e gastos.")

    # INVESTIMENTO + GRÁFICO
    if "investimento" in intencoes:
        partes.append("""
Investimento funciona com consistência.

Exemplo:
R$200/mês → 10 anos ≈ R$40 mil

Veja o simulador na lateral para testar valores reais.
""")

    # GASTOS
    if "gastos" in intencoes:
        partes.append("""
Controle:
- anote tudo
- corte excessos
- mantenha disciplina
""")

    # RENDA EXTRA
    if "renda" in intencoes:
        partes.append("""
Renda extra:
- freelance
- revenda
- internet
""")

    # RIQUEZA
    if "riqueza" in intencoes:
        partes.append("""
Riqueza = tempo + investimento + consistência
""")

    if not partes:
        return "Seja mais específico ou envie números."

    return "\n".join(partes)

# =========================
# CHAT
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            time.sleep(1)
            resposta = responder(prompt)
            st.markdown(resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})
