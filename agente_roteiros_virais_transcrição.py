import os
import streamlit as st
from openai import OpenAI

# ==========================================
# Proteção contra versões incorretas do pacote openai
# ==========================================
os.system("pip install --upgrade --force-reinstall openai==1.44.0 > /dev/null 2>&1")

# ==========================================
# Função principal de geração de roteiro
# ==========================================

def gerar_roteiro(transcricao: str, api_key: str):
    """Transforma a transcrição em um roteiro viral completo e fiel."""
    client = OpenAI(api_key=api_key)

    prompt = f"""
Você é um roteirista especialista em vídeos virais com alta retenção.
Sua missão é transformar a transcrição abaixo em um roteiro no formato viral, **sem perder nenhum detalhe real** e **mantendo a ordem cronológica**.

🎯 OBJETIVO:
Criar um roteiro que conte todas as histórias e informações da transcrição de forma envolvente, emocional e cinematográfica — mas sem alterar ou omitir fatos, nomes, números, espécies, locais, datas ou qualquer dado real.

⚠️ REGRAS OBRIGATÓRIAS:
1. **Todos os dados reais da transcrição devem aparecer no roteiro.**
   - Inclua nomes, números, locais, datas, espécies, medidas, termos científicos, curiosidades e comparações.
   - Não simplifique nem generalize fatos (ex: se disser “Ochotona, gênero de mamíferos da família Ochotonidae”, mantenha exatamente isso no roteiro).
2. **Não invente fatos.**
3. **Respeite a ordem cronológica do vídeo original.**
4. **Estilo narrativo:** linguagem natural, fluida e emocional, como em vídeos documentais virais.
5. **Ritmo:** frases curtas, interrogações, pausas dramáticas e ganchos a cada 20–30 segundos.
6. **Estrutura sugerida:**

Início:
   - 5 segundos que reflitam a thumb (impacto e curiosidade)
   - Até 30 segundos de contexto e questionamento inicial

Meio (pode conter vários blocos, até cobrir todas as histórias):
   - Cada bloco (até 90 segundos) deve:
       a) Alternar entre momentos opostos (ex: descoberta vs dúvida, sucesso vs fracasso)
       b) Fechar com uma resposta surpreendente, insight ou virada
   - Continue criando novos blocos até representar todo o conteúdo da transcrição

Fim:
   - Recompensa final: opinião ou conclusão emocional sobre a jornada
   - CTA de engajamento (seguir, curtir, comentar, etc.)

7. **No final do roteiro, adicione também:**
   - 🎬 **Título chamativo**
   - 🖼️ **Ideia de Thumb (imagem + texto)**
   - 🎞️ **3 ideias de Shorts**
   - ✂️ **3 sugestões de edição (efeitos, cortes, transições)**

Transcrição original:
\"\"\"{transcricao}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erro ao gerar roteiro: {e}")
        return None


# ==========================================
# Interface Streamlit
# ==========================================

st.set_page_config(page_title="Agente de Roteiros Virais (modo texto)", page_icon="🎬", layout="wide")

st.title("🎬 Agente de Roteiros Virais (modo texto)")

st.caption("Transforme transcrições em roteiros virais envolventes e fiéis aos fatos originais.")

st.divider()

st.markdown("#### 🔑 Insira sua OpenAI API Key:")
api_key = st.text_input("API Key", type="password")

st.markdown("#### 📝 Cole a transcrição completa do vídeo:")
transcricao = st.text_area("Cole aqui o texto completo da transcrição:", height=300)

if st.button("Gerar Roteiro"):
    if not api_key:
        st.error("Por favor, insira sua chave da OpenAI.")
    elif not transcricao.strip():
        st.error("Por favor, cole a transcrição antes de gerar o roteiro.")
    else:
        progress = st.progress(0)
        with st.spinner("🧠 Processando roteiro..."):
            progress.progress(50)
            roteiro = gerar_roteiro(transcricao, api_key)
            progress.progress(100)

        if roteiro:
            st.success("✅ Roteiro gerado com sucesso!")
            st.markdown("### 🎯 Roteiro Viral Final")
            st.write(roteiro)
        else:
            st.error("❌ Não foi possível gerar o roteiro.")
