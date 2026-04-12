import streamlit as st
import time

st.set_page_config(page_title="Finix IA", page_icon="💰")

st.title("💰 Finix IA")
st.caption("Finix IA v1.0 | Assistente financeiro inteligente")

# =========================
# Funções
# =========================

def calcular_juros_compostos(valor, taxa, tempo):
    return valor * (1 + taxa) ** tempo

def responder(pergunta):
    p = pergunta.lower()

    if "planejamento" in p or "organizar dinheiro" in p:
        return """
📊 Planejamento Financeiro

Organizar seu dinheiro é simples se seguir um método:

1) Descubra quanto sobra no mês  
Subtraia seus gastos da sua renda.

2) Divida sua sobra:
- 50% Investimentos
- 30% Reserva de emergência
- 20% Lazer

Exemplo:
Renda: R$2000  
Gastos: R$1200  
Sobra: R$800  

Divisão:
- R$400 investimentos  
- R$240 reserva  
- R$160 lazer  

Isso cria equilíbrio entre futuro e presente.
"""

    elif "investimento" in p or "juros" in p:
        return """
💸 Juros Compostos

Juros compostos fazem seu dinheiro crescer sozinho com o tempo.

Exemplo:
Investindo R$1000 a 10% ao ano:

- 1 ano: R$1100  
- 5 anos: R$1610  
- 10 anos: R$2590  

Agora imagine investir todo mês:

R$200/mês por 10 anos → +R$40.000

Conclusão:
Tempo + consistência = crescimento exponencial
"""

    elif "ficar rico" in p or "enriquecer" in p:
        return """
🧠 Como enriquecer

Não é sorte, é estratégia:

1) Aumentar renda
Aprenda habilidades valorizadas (programação, vendas, design)

2) Investir sempre
Mesmo valores pequenos fazem diferença

3) Tempo
Quanto antes começar, melhor

Exemplo:
R$200/mês a 10% ao ano:
→ em 10 anos ≈ R$40.000

Resumo:
Disciplina > Motivação
"""

    elif "gastos" in p:
        return """
📉 Controle de Gastos

Método prático:

1) Anote tudo por 30 dias
Ex:
- Lanche: R$15  
- Uber: R$20  
- Assinaturas: R$30  

2) Separe:
- Necessário  
- Supérfluo  

3) Corte 20% do supérfluo

Exemplo:
R$500 gastos desnecessários  
→ corta 20% = R$100/mês  

Em 1 ano:
→ R$1200 economizados

Esse dinheiro pode virar investimento.
"""

    elif "renda extra" in p:
        return """
💼 Renda Extra

Formas reais de ganhar dinheiro:

1) Freelance
- Design, edição, programação

2) Revenda
Comprar barato e vender mais caro

3) Internet
Criar conteúdo ou produtos digitais

Exemplo:
Compra por R$20 → vende por R$40  
Lucro: R$20 por unidade

Importante:
Prefira algo que possa crescer (escala).
"""

    else:
        return """
❓ Não entendi totalmente sua pergunta.

Você pode perguntar sobre:
- planejamento financeiro  
- investimentos  
- gastos  
- renda extra  

Tente algo mais específico.
"""

# =========================
# Chat (estilo ChatGPT)
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua pergunta..."):
    
    # salva usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # simula "pensando"
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            time.sleep(1)
            resposta = responder(prompt)
            st.markdown(resposta)

    # salva resposta
    st.session_state.messages.append({"role": "assistant", "content": resposta})
