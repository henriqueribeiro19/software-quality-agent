import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def gerar_codigo(prompt, modelo="mixtral-8x7b-32768", temperatura=0.3, mensagens_extra=None):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    mensagens = [{"role": "user", "content": prompt}]
    if mensagens_extra:
        mensagens = mensagens_extra + mensagens

    payload = {
        "model": modelo,
        "messages": mensagens,
        "temperature": temperatura
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        return f"❌ Erro HTTP: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Erro de conexão: {str(e)}"
    except KeyError:
        return "❌ Erro ao interpretar resposta da API."
