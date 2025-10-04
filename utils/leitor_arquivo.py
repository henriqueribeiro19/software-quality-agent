def ler_arquivo(uploaded_file):
    try:
        return uploaded_file.read().decode("utf-8")
    except Exception as e:
        return f"❌ Erro ao ler arquivo: {e}"
