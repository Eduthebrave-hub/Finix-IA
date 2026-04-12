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
Assistente financeiro estratégico baseado em análise real
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
        st.session_state.renda = None
        st.session_state.gastos = None
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
# RESPOSTA INTELIGENTE
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

    renda = st.session_state.get("renda", None)
    gastos = st.session_state.get("gastos", None)

    # =========================
    # PLANEJAMENTO
    # =========================
    if "planejamento" in intencoes:
        if renda is not None and gastos is not None:
            sobra = renda - gastos

            if sobra <= 0:
                partes.append(f"""
📊 Situação atual:

Você ganha R${renda} e gasta R${gastos}.

Resultado: você está no negativo.

📉 Problema:
Sem sobra, não existe investimento nem crescimento financeiro.

✔️ Ação imediata:
- cortar gastos
- eliminar excessos
- buscar renda extra

Exemplo:
Reduzir R$300 já muda seu cenário.

Conclusão:
Primeiro parar de perder, depois crescer.
""")
            else:
                investir = sobra * 0.5
                reserva = sobra * 0.3
                lazer = sobra * 0.2

                partes.append(f"""
📊 Análise completa:

Renda: R${renda}  
Gastos: R${gastos}  
Sobra: R${sobra}  

💡 Estratégia:

- Investir: R${investir:.0f}
- Reserva: R${reserva:.0f}
- Lazer: R${lazer:.0f}

📈 Explicação:
Investimentos fazem seu dinheiro crescer.  
Reserva protege contra imprevistos.  
Lazer evita desistência.

📊 Exemplo:
Investindo R${investir:.0f}/mês por anos → crescimento exponencial.

Conclusão:
Você já está em posição de evolução.

Quer que eu simule o crescimento?
""")
        else:
            partes.append("""
Preciso dos seus números.

Exemplo:
"ganho 2000 e gasto 1200"
""")

    # =========================
    # INVESTIMENTO
    # =========================
    if "investimento" in intencoes:
        partes.append("""
💸 Investimento:

Base = consistência.

Exemplo:
R$200/mês  
10 anos → ~R$40.000  

Quanto antes começar, melhor.

Tempo > dinheiro inicial.
""")

    # =========================
    # GASTOS
    # =========================
    if "gastos" in intencoes:
        partes.append("""
📉 Controle de gastos:

1. anotar tudo  
2. separar necessário/supérfluo  
3. cortar 20%

Resultado:
mais dinheiro livre todo mês.
""")

    # =========================
    # RENDA EXTRA
    # =========================
    if "renda" in intencoes:
        partes.append("""
💼 Renda extra:

- Freelance
- Revenda
- Internet

Foque no que pode crescer.
""")

    # =========================
    # RIQUEZA
    # =========================
    if "riqueza" in intencoes:
        partes.append("""
🧠 Riqueza:

Renda + investimento + tempo.

Sem consistência, não existe resultado.
""")

    # FALLBACK
    if not partes:
        return """
Seja mais específico.

Exemplo:
"ganho 2000 e gasto 1200"
ou
"como investir?"
"""

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
