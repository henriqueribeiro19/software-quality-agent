import os

def dividir_conteudo(texto, tamanho=800):
    """
    Divide o texto em blocos menores para evitar limite de tokens.
    
    Args:
        texto (str): Texto a ser dividido.
        tamanho (int): Quantidade de linhas por chunk.

    Returns:
        generator: partes do texto divididas
    """
    linhas = texto.splitlines()
    for i in range(0, len(linhas), tamanho):
        yield "\n".join(linhas[i:i + tamanho])


def ler_projeto_completo(pasta_raiz, extensoes=None, limite=50):
    """
    Lê arquivos de uma pasta e suas subpastas com filtros por extensão e limite.
    Divide arquivos grandes em partes menores (chunks).

    Args:
        pasta_raiz (str): Caminho da pasta raiz do projeto.
        extensoes (list): Lista de extensões permitidas (ex: [".py", ".md"]).
        limite (int): Número máximo de arquivos/chunks a ler.

    Returns:
        dict: {caminho_absoluto: conteúdo_do_arquivo ou chunk}
    """
    if extensoes is None:
        extensoes = [".py", ".md", ".txt", ".yaml", ".yml", ".sh", ".env", ".json"]

    arquivos_lidos = {}
    contador = 0

    for raiz, _, arquivos in os.walk(pasta_raiz):
        for nome in arquivos:
            if contador >= limite:
                break
            if any(nome.endswith(ext) for ext in extensoes):
                caminho = os.path.join(raiz, nome)
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        conteudo = f.read()

                        # Se o arquivo for muito grande, divide em partes
                        for idx, parte in enumerate(dividir_conteudo(conteudo)):
                            chave = caminho if idx == 0 else f"{caminho} (parte {idx+1})"
                            arquivos_lidos[chave] = parte
                            contador += 1
                            if contador >= limite:
                                break
                except Exception as e:
                    arquivos_lidos[caminho] = f"❌ Erro ao ler: {e}"

    return arquivos_lidos
