import streamlit as st
import tempfile
import os
from openai import OpenAI
import openai as openai_module  # usado só para mostrar versão opcionalmente

# ---------- Helper: show openai version (debug) ------------
def _openai_version():
    try:
        return getattr(openai_module, "__version__", "unknown")
    except Exception:
        return "unknown"

# ---------- Roteiro generator (usa novo cliente OpenAI) ----
def gerar_roteiro(transcricao: str, api_key: str):
    """
    Gera roteiro viral com o cliente OpenAI moderno.
    Instancia OpenAI(api_key=...) e chama client.chat.completions.create(...)
    """
    # Cria cliente explicitamente (não setar openai.api_key globalmente)
    try:
        client = OpenAI(api_key=api_key)
    except TypeError as e:
        # Provavelmente instalação inválida da lib openai (ex: pacote conflitante)
        raise RuntimeError(
            "Erro ao inicializar OpenAI client. "
            "Provavelmente há uma versão/instalação incompatível da biblioteca `openai`.\n"
            "Verifique se instalou `openai==1.44.0` e não outro pacote chamado `openai`.\n"
            "Mensagem original: " + str(e)
        ) from e

    prompt = f"""
Você é um roteirista especialista em vídeos virais com alta retenção.
Sua missão é transformar a transcrição abaixo em um roteiro no formato viral, sem perder detalhes reais e mantendo ordem cronológica.

Regras (resuma em linguagem curta, levando fatos):
- Inclua nomes, datas, locais e fatos explicitamente presentes na transcrição.
- Não invente fatos.
- Use blocos de até 90s revezando momentos opostos e respostas.
- Inicio (5s hook + até 30s contexto), meio (vários blocos), fim (opinião + CTA).
- Ao final entregue também: Título chamativo, ideia de thumb, 3 ideias de Shorts, 3 sugestões de edição.

Transcrição:
\"\"\"{transcricao}\"\"\"
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um roteirista criativo e preciso."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1800
        )
        # novo SDK: resposta em resp.choices[0].message.content
        return resp.choices[0].message.content
    except TypeError as e:
        # capturamos casos estranhos de incompatibilidade (ex: proxies arg)
        raise RuntimeError(
            "Erro ao chamar a API ChatCompletion (provável conflito de versão do SDK `openai`).\n"
            "Sugestão: reinstale a versão oficial: `pip install --upgrade openai==1.44.0`\n"
            "Se estiver no Streamlit Cloud, atualize requirements.txt e redeploy.\n"
            "Mensagem original: " + str(e)
        ) from e
    except Exception as e:
        # repassa erro para UI
        raise RuntimeError(f"Erro durante a chamada à API da OpenAI: {e}") from e


# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Agente de Roteiros Virais (texto)", layout="centered")
st.title("🎬 Agente de Roteiros Virais (modo texto)")

st.markdown("**Debug:** OpenAI lib version: `" + _openai_version() + "`")

api_key = st.text_input("🔑 Insira sua OpenAI API Key:", type="password")
transcricao = st.text_area("📝 Cole a transcrição do vídeo aqui (texto completo):", height=360)

if st.button("Gerar Roteiro"):
    if not api_key:
        st.error("Insira sua chave da OpenAI.")
    elif not transcricao or not transcricao.strip():
        st.error("Cole a transcrição do vídeo no campo de texto.")
    else:
        with st.spinner("Gerando roteiro..."):
            try:
                roteiro = gerar_roteiro(transcricao, api_key)
                st.success("✅ Roteiro gerado com sucesso!")
                st.markdown("### 🎯 Roteiro Viral")
                st.write(roteiro)
                st.download_button("📥 Baixar roteiro (.txt)", roteiro, file_name="roteiro_viral.txt")
            except RuntimeError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
