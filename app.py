import streamlit as st
import time
import re

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
    font-size: 2.5rem;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
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
# SIDEBAR
# =========================
with st.sidebar:
    st.header("📊 Painel")

    renda = st.session_state.get("renda", "—")
    gastos = st.session_state.get("gastos", "—")

    st.write(f"**Renda:** R${renda}")
    st.write(f"**Gastos:** R${gastos}")

    if st.button("Limpar conversa"):
        st.session_state.messages = []
        st.rerun()

# =========================
# INTENÇÕES
# =========================
def detectar_intencoes(p):
    intents = {
        "saudacao": ["oi", "olá", "eae", "fala"],
        "planejamento": ["organizar", "planejamento", "finanças", "dinheiro"],
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

    if "saudacao" in intencoes:
        partes.append("Tudo sob controle.")

    if len(numeros) >= 2:
        st.session_state["renda"] = numeros[0]
        st.session_state["gastos"] = numeros[1]

    renda = st.session_state.get("renda")
    gastos = st.session_state.get("gastos")

    if "planejamento" in intencoes:
        if renda is not None and gastos is not None:
            sobra = renda - gastos
            if sobra <= 0:
                partes.append(f"""
Renda: R${renda}
Gastos: R${gastos}

Você está no negativo.
""")
            else:
                partes.append(f"""
Renda: R${renda}
Gastos: R${gastos}
Sobra: R${sobra}

→ Investir: R${sobra*0.5:.0f}
→ Reserva: R${sobra*0.3:.0f}
→ Lazer: R${sobra*0.2:.0f}
""")
        else:
            partes.append("Me diga sua renda e gastos.")

    if "investimento" in intencoes:
        partes.append("""
Exemplo:
R$200/mês → 10 anos ≈ R$40 mil

Consistência é o principal fator.
""")

    if "gastos" in intencoes:
        partes.append("""
Anote tudo por 30 dias.
Corte 20% do desnecessário.
""")

    if "renda" in intencoes:
        partes.append("""
Renda extra:
- Freelance
- Revenda
- Internet
""")

    if "riqueza" in intencoes:
        partes.append("""
Riqueza = tempo + investimento + renda
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
