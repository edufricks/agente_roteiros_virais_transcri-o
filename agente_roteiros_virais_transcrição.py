import streamlit as st
from openai import OpenAI

# ==============================
# Função principal
# ==============================
def gerar_roteiro(transcricao: str, api_key: str):
    """Transforma a transcrição em um roteiro viral fiel e envolvente."""
    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
Você é um roteirista especialista em vídeos virais com alta retenção.
Sua missão é transformar a transcrição abaixo em um roteiro no formato viral, **sem perder nenhum detalhe real** e **mantendo a ordem cronológica**.

🎯 OBJETIVO:
Criar um roteiro que conte todas as histórias e informações da transcrição de forma envolvente, emocional e cinematográfica — mas sem alterar ou omitir fatos, nomes, números, espécies, locais, datas ou qualquer dado real.

⚠️ REGRAS OBRIGATÓRIAS:
1. **Todos os dados reais da transcrição devem aparecer no roteiro.**
   - Inclua nomes, números, locais, datas, espécies, medidas, termos científicos, curiosidades e comparações.
2. **Não invente fatos.**
3. **Respeite a ordem cronológica.**
4. **Estilo:** natural, fluido e emocional (como documentário viral).
5. **Ritmo:** frases curtas, pausas dramáticas, ganchos a cada 20–30 segundos.
6. **Estrutura:**
   - Início: 5s de impacto e 30s de contexto/questionamento.
   - Meio: blocos de até 90s com viradas ou descobertas.
   - Fim: recompensa emocional + CTA.
7. **Finalize com:**
   - 🎬 Título chamativo
   - 🖼️ Ideia de Thumb
   - 🎞️ 3 ideias de Shorts
   - ✂️ 3 sugestões de edição

Transcrição original:
\"\"\"{transcricao}\"\"\"
"""

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return resposta.choices[0].message.content

    except Exception as e:
        st.error(f"Erro ao gerar roteiro: {e}")
        return None


# ==============================
# Interface Streamlit
# ==============================
st.set_page_config(page_title="Agente de Roteiros Virais (modo texto)", page_icon="🎬", layout="wide")

st.title("🎬 Agente de Roteiros Virais (modo texto)")
st.caption("Transforme transcrições em roteiros virais envolventes e fiéis aos fatos originais.")
st.divider()

api_key = st.text_input("🔑 Digite sua chave da OpenAI:", type="password")
transcricao = st.text_area("📋 Cole a transcrição completa do vídeo aqui:", height=300)

if st.button("Gerar Roteiro"):
    if not api_key:
        st.error("Por favor, insira sua chave da OpenAI.")
    elif not transcricao.strip():
        st.error("Por favor, cole a transcrição antes de gerar o roteiro.")
    else:
        progress = st.progress(0)
        with st.spinner("🧠 Gerando roteiro..."):
            progress.progress(50)
            roteiro = gerar_roteiro(transcricao, api_key)
            progress.progress(100)

        if roteiro:
            st.success("✅ Roteiro gerado com sucesso!")
            st.markdown("### 🎯 Roteiro Viral Final")
            st.write(roteiro)
        else:
            st.error("❌ Não foi possível gerar o roteiro.")
