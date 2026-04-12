import re
import streamlit as st

# =========================
# INTENÇÕES
# =========================
def detectar_intencoes(p):
    intents = {
        "saudacao": ["oi", "olá", "eae", "fala", "bom dia", "boa tarde"],
        "planejamento": ["planejamento", "organizar", "controlar", "finanças", "dinheiro"],
        "investimento": ["investir", "investimento", "juros", "aplicar"],
        "gastos": ["gastos", "despesas", "gastar"],
        "renda_extra": ["renda extra", "ganhar dinheiro", "extra"],
        "riqueza": ["rico", "enriquecer", "riqueza"]
    }

    encontrados = []

    for intent, palavras in intents.items():
        for palavra in palavras:
            if palavra in p:
                encontrados.append(intent)
                break

    return encontrados


# =========================
# EXTRAIR NÚMEROS
# =========================
def extrair_numeros(p):
    numeros = re.findall(r'\d+', p)
    return [int(n) for n in numeros]


# =========================
# RESPOSTA PRINCIPAL
# =========================
def responder(pergunta):
    p = pergunta.lower()

    intencoes = detectar_intencoes(p)
    numeros = extrair_numeros(p)

    partes = []

    # =========================
    # SAUDAÇÃO
    # =========================
    if "saudacao" in intencoes:
        partes.append("Tudo sob controle.")

    # =========================
    # SALVAR DADOS
    # =========================
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

Renda: R${renda}
Gastos: R${gastos}

Você está no negativo.
Prioridade: cortar gastos.
""")
            else:
                investir = sobra * 0.5
                reserva = sobra * 0.3
                lazer = sobra * 0.2

                partes.append(f"""
📊 Plano financeiro:

Renda: R${renda}
Gastos: R${gastos}
Sobra: R${sobra}

Divisão:
→ Investir: R${investir:.0f}
→ Reserva: R${reserva:.0f}
→ Lazer: R${lazer:.0f}

Estratégia simples, mas eficiente.
""")
        else:
            partes.append("""
Preciso dos seus dados.

Exemplo:
"ganho 2000 e gasto 1200"
""")

    # =========================
    # INVESTIMENTO
    # =========================
    if "investimento" in intencoes:
        partes.append("""
💸 Investimento:

Consistência > valor inicial

Exemplo:
R$200/mês a 10% ao ano:
→ 10 anos ≈ R$40.000

Quanto você conseguiria investir por mês?
""")

    # =========================
    # GASTOS
    # =========================
    if "gastos" in intencoes:
        partes.append("""
📉 Controle de gastos:

1. Anote tudo por 30 dias
2. Corte 20% do desnecessário

R$100/mês economizados = R$1200/ano
""")

    # =========================
    # RENDA EXTRA
    # =========================
    if "renda_extra" in intencoes:
        partes.append("""
💼 Renda extra:

- Freelance
- Revenda
- Internet

Prefira algo escalável.
""")

    # =========================
    # RIQUEZA
    # =========================
    if "riqueza" in intencoes:
        partes.append("""
🧠 Riqueza:

Renda + investimento + tempo

Sem consistência, não funciona.
""")

    # =========================
    # SE TEM NÚMEROS MAS SEM INTENÇÃO
    # =========================
    if len(numeros) >= 2 and "planejamento" not in intencoes:
        partes.append("""
Quer que eu monte um planejamento com esses números?
""")

    # =========================
    # FALLBACK
    # =========================
    if not partes:
        return """
Seja mais específico.

Exemplos:
- "ganho 2000 e gasto 1200"
- "como investir?"
- "como organizar meu dinheiro?"
"""

    return "\n".join(partes)
