import re

# =========================
# INTENÇÕES
# =========================
def detectar_intencoes(p):
    intents = {
        "saudacao": ["oi", "olá", "eae", "fala", "bom dia", "boa tarde"],
        "planejamento": ["planejamento", "organizar", "controlar", "finanças", "dinheiro"],
        "investimento": ["investir", "investimento", "juros", "aplicar"],
        "gastos": ["gastos", "despesas", "gastar"],
        "renda": ["renda", "ganhar dinheiro", "renda extra"],
        "riqueza": ["rico", "enriquecer"]
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

    resposta = ""

    # =========================
    # SAUDAÇÃO
    # =========================
    if "saudacao" in intencoes:
        resposta += "Tudo sob controle. "

    # =========================
    # SE TEM NÚMEROS → SALVA MEMÓRIA
    # =========================
    if len(numeros) >= 2:
        st.session_state["renda"] = numeros[0]
        st.session_state["gastos"] = numeros[1]

    # =========================
    # PLANEJAMENTO COM DADOS
    # =========================
    if "planejamento" in intencoes:
        renda = st.session_state.get("renda")
        gastos = st.session_state.get("gastos")

        if renda and gastos:
            sobra = renda - gastos

            if sobra <= 0:
                resposta += f"""
Você está no negativo.

Renda: R${renda}
Gastos: R${gastos}

Corte custos antes de pensar em investir.
"""
            else:
                investir = sobra * 0.5
                reserva = sobra * 0.3
                lazer = sobra * 0.2

                resposta += f"""
Plano baseado nos seus dados:

Renda: R${renda}
Gastos: R${gastos}
Sobra: R${sobra}

Distribuição:
→ Investir: R${investir:.0f}
→ Reserva: R${reserva:.0f}
→ Lazer: R${lazer:.0f}

Se manter isso, você evolui financeiramente.
"""
        else:
            resposta += """
Para montar um plano, preciso dos seus números.

Exemplo:
"ganho 2000 e gasto 1200"
"""

    # =========================
    # INVESTIMENTO
    # =========================
    if "investimento" in intencoes:
        resposta += """

Investimento depende de consistência.

Exemplo:
R$200/mês a 10% ao ano:
→ 10 anos ≈ R$40 mil

Quanto você conseguiria investir por mês?
"""

    # =========================
    # GASTOS
    # =========================
    if "gastos" in intencoes:
        resposta += """

Controle de gastos:

Anote tudo por 30 dias  
Corte 20% do desnecessário  

R$100 economizados/mês = R$1200/ano
"""

    # =========================
    # RENDA EXTRA
    # =========================
    if "renda" in intencoes:
        resposta += """

Renda extra:

- Freelance  
- Revenda  
- Internet  

Prefira algo escalável.
"""

    # =========================
    # RIQUEZA
    # =========================
    if "riqueza" in intencoes:
        resposta += """

Riqueza = renda + investimento + tempo.

Sem consistência, não funciona.
"""

    # =========================
    # SE NADA DETECTADO
    # =========================
    if resposta.strip() == "":
        resposta = """
Seja mais direto.

Ou me manda números que eu analiso.
"""

    return resposta
