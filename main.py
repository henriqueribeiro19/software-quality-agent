import streamlit as st
import os
from utils.groq_client import gerar_codigo
from utils.leitor_projeto import ler_projeto_completo
from utils.leitor_arquivo import ler_arquivo
from utils.prompts import prompt_analise_projeto

st.set_page_config(page_title="Software Quality Agent", layout="wide")
st.title("🧠 Siri Ema Test Lab")

# -------------------------------
# 💾 Histórico de Mensagens
# -------------------------------
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

def adicionar_mensagem(role, content):
    st.session_state["mensagens"].append({"role": role, "content": content})

# -------------------------------
# 🎛️ Sidebar: Configurações
# -------------------------------
st.sidebar.header("⚙️ Configurações")

modelos_disponiveis = {
    "LLama-Versatile":"llama-3.3-70b-versatile",
    "LLaMA 3 (8B)": "llama3-8b-8192",
    "Mixtral (8x7B)": "mixtral-8x7b-32768"
}
modelo_selecionado = st.sidebar.selectbox("🧠 Modelo de IA", list(modelos_disponiveis.keys()))
modelo_id = modelos_disponiveis[modelo_selecionado]

temperatura = st.sidebar.slider("🔥 Temperatura da IA", 0.0, 1.0, 0.3, 0.1)
usar_historico = st.sidebar.checkbox("🧠 Usar histórico de mensagens", value=False)
modo_comparativo = st.sidebar.checkbox("🧪 Comparar modelos lado a lado", value=False)

tipos = st.sidebar.multiselect(
    "📄 Tipos de arquivos para incluir",
    [".py", ".md", ".txt", ".yaml", ".yml", ".sh", ".env", ".json"],
    default=[".py", ".md"]
)
limite = st.sidebar.slider("📊 Limite de arquivos para análise", 10, 200, 50)

# -------------------------------
# 🔀 Navegação por abas
# -------------------------------
abas = st.tabs([
    "💡 Gerar Código",
    "🧠 Explicar Código",
    "📁 Analisar Arquivo",
    "📂 Análise de Projeto",
    "⚡ Corrigir Código"
])


# -------------------------------
# 💡 Aba 1: Gerar Código
# -------------------------------
with abas[0]:
    st.subheader("💡 Gerador de Código")
    prompt = st.text_area("Descreva o que você quer que o código faça:", height=200)
    if st.button("Gerar código", key="btn_gerar_codigo"):
        with st.spinner("Gerando..."):
            if modo_comparativo:
                resposta_1 = gerar_codigo(prompt, modelo="llama3-8b-8192", temperatura=temperatura)
                resposta_2 = gerar_codigo(prompt, modelo="mixtral-8x7b-32768", temperatura=temperatura)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 🧠 LLaMA 3")
                    st.code(resposta_1, language="python")
                with col2:
                    st.markdown("### 🧠 Mixtral")
                    st.code(resposta_2, language="python")
            else:
                resposta = gerar_codigo(prompt, modelo=modelo_id, temperatura=temperatura)
                st.code(resposta, language="python")
    st.divider()

# -------------------------------
# 🧠 Aba 2: Explicação de Código
# -------------------------------
with abas[1]:
    st.subheader("🧠 Explicação de Código")
    codigo = st.text_area("Cole o código que deseja entender:", height=200)
    if st.button("Explicar", key="btn_explicar_codigo"):
        with st.spinner("Explicando..."):
            prompt_explicacao = f"""
Você é um especialista em engenharia de software. Explique detalhadamente o seguinte código Python, destacando:

- O que ele faz
- Possíveis erros ou riscos
- Sugestões de melhoria

Código:
{codigo}
"""
            mensagens_extra = [{"role": "system", "content": "Você é um especialista em qualidade de software."}]
            resposta = gerar_codigo(
                prompt_explicacao,
                modelo=modelo_id,
                temperatura=temperatura,
                mensagens_extra=mensagens_extra if usar_historico else None
            )
            st.markdown("### 📝 Explicação")
            st.write(resposta)
    st.divider()

# -------------------------------
# 📁 Aba 3: Upload de Arquivo
# -------------------------------
with abas[2]:
    st.subheader("📁 Upload de Arquivo para Análise")
    arquivo = st.file_uploader("Envie um arquivo `.py` ou `.txt`", type=["py", "txt"])
    if arquivo is not None:
        conteudo = ler_arquivo(arquivo)
        st.code(conteudo, language="python")
        if st.button("Analisar Arquivo", key="btn_analisar_arquivo"):
            with st.spinner("Analisando..."):
                prompt_arquivo = f"""
Você é um especialista em qualidade de software. Analise o seguinte código e identifique:

1. Possíveis erros de codificação
2. Más práticas de estrutura ou lógica
3. Sugestões de melhoria
4. Classificação dos problemas por gravidade (leve, moderado, crítico)

Código:
{conteudo}
"""
                resposta = gerar_codigo(prompt_arquivo, modelo=modelo_id, temperatura=temperatura)
                st.markdown("### 🔍 Análise do Arquivo")
                st.write(resposta)
    st.divider()

# -------------------------------
# 📂 Aba 4: Análise de Projeto Completo
# -------------------------------
with abas[3]:
    st.subheader("📂 Análise de Projeto Completo")
    caminho_pasta = st.text_input("📌 Cole o caminho da pasta do projeto:")

    if caminho_pasta and os.path.isdir(caminho_pasta):
        arquivos = ler_projeto_completo(caminho_pasta, extensoes=tipos, limite=limite)
        st.success(f"{len(arquivos)} arquivos encontrados com os filtros selecionados.")

        if st.button("Analisar Projeto", key="btn_analisar_projeto_etapas"):
            with st.spinner("Analisando projeto filtrado..."):
                conteudo_total = "\n\n".join([f"{k}:\n{v}" for k, v in arquivos.items()])
                prompt = prompt_analise_projeto(conteudo_total)
                resposta = gerar_codigo(prompt, modelo=modelo_id, temperatura=temperatura)
                st.markdown("### 🧠 Relatório de Qualidade do Projeto")
                st.write(resposta)
    elif caminho_pasta:
        st.error("❌ Caminho inválido. Verifique se a pasta existe.")

# -------------------------------
# ⚡ Aba 5: Corrigir Código
# -------------------------------
with abas[4]:
    st.subheader("⚡ Refatorar / Corrigir Código")
    codigo_corrigir = st.text_area("Cole o código que deseja corrigir/refatorar:", height=250)

    opcoes = st.multiselect(
        "Escolha os focos de correção",
        ["Erros de execução", "Segurança", "Performance", "Boas práticas (SOLID/DRY)", "Documentação e testes"],
        default=["Erros de execução", "Boas práticas (SOLID/DRY)"]
    )

    if st.button("Corrigir Código", key="btn_corrigir_codigo"):
        with st.spinner("Refatorando..."):
            prompt_corrigir = f"""
Você é um engenheiro de software especialista em qualidade de código.
Recebeu o seguinte código e deve devolver uma **versão corrigida/refatorada**, considerando os pontos abaixo:

Foco da correção: {", ".join(opcoes)}

Código original:
{codigo_corrigir}

Responda apenas com o código corrigido, sem explicações extras.
"""
            resposta_corrigida = gerar_codigo(
                prompt_corrigir,
                modelo=modelo_id,
                temperatura=0.2,
                mensagens_extra=st.session_state["mensagens"] if usar_historico else None
            )

            st.markdown("### ✅ Código Refatorado")
            st.code(resposta_corrigida, language="python")

            # salva no histórico
            adicionar_mensagem("user", prompt_corrigir)
            adicionar_mensagem("assistant", resposta_corrigida)

