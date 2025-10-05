import streamlit as st
import openai

# ==========================================
# Função principal para gerar o roteiro
# ==========================================
def gerar_roteiro(transcricao: str, api_key: str):
    """Gera o roteiro final no formato viral respeitando a cronologia."""
    openai.api_key = api_key

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
   - Pode melhorar a forma de contar, mas nunca criar informações novas.
3. **Respeite a ordem cronológica do vídeo original.**
4. **Estilo narrativo:** linguagem natural, fluida e emocional, como em vídeos documentais virais ou narrativas do YouTube.
5. **Ritmo:** frases curtas, interrogações, pausas dramáticas e ganchos a cada 20–30 segundos.
6. **Estrutura sugerida:**

Início:
   - 5 segundos que reflitam a thumb (impacto e curiosidade)
   - Até 30 segundos de contexto e questionamento inicial

Meio (pode conter vários blocos, até cobrir todas as histórias):
   - Cada bloco (até 90 segundos) deve:
       a) Alternar entre momentos opostos (ex: descoberta vs dúvida, sucesso vs fracasso, fragilidade vs superação)
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

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


# ==========================================
# Interface Streamlit
# ==========================================
st.title("🎬 Agente de Roteiros Virais (modo texto)")
st.write("Cole abaixo a transcrição completa do vídeo para gerar um roteiro no formato viral.")

api_key = st.text_input("🔑 Digite sua chave da OpenAI:", type="password")
transcricao = st.text_area("📝 Cole aqui a transcrição completa do vídeo:", height=300)

if st.button("Gerar Roteiro"):
    if not api_key:
        st.error("Por favor, insira sua chave da OpenAI.")
    elif not transcricao.strip():
        st.error("Por favor, cole a transcrição do vídeo.")
    else:
        with st.spinner("✨ Gerando roteiro viral com base na transcrição..."):
            try:
                roteiro = gerar_roteiro(transcricao, api_key)
                st.success("✅ Roteiro gerado com sucesso!")
                st.markdown("### 🎯 Roteiro Viral")
                st.write(roteiro)

                st.download_button(
                    "📥 Baixar roteiro em .txt",
                    roteiro,
                    file_name="roteiro_viral.txt"
                )
            except Exception as e:
                st.error(f"❌ Erro ao gerar roteiro: {e}")
