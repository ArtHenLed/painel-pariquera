import os
import requests

# --- CONFIGURAÇÃO ---
API_KEY = os.getenv("OPENWEATHER_API_KEY") 
CIDADE = "Pariquera-Açu" # Nome da cidade para a API
ESTADO = "BR"
ARQUIVO_BASE = "relogio_clima_base.html"
ARQUIVO_SAIDA = "index.html" # Arquivo final que o Netlify vai mostrar

# Monta a URL da API para buscar o tempo atual
url_api = f"https://api.openweathermap.org/data/2.5/weather?q={CIDADE},{ESTADO}&appid={API_KEY}&units=metric&lang=pt_br"

try:
    # --- BUSCA OS DADOS DO CLIMA ---
    response = requests.get(url_api)
    response.raise_for_status() # Lança um erro se a requisição falhar
    dados_clima = response.json()

    temperatura = round(dados_clima['main']['temp'])
    condicao = dados_clima['weather'][0]['description']
    icone_id = dados_clima['weather'][0]['icon']
    url_icone = f"https://openweathermap.org/img/wn/{icone_id}@2x.png"

    # --- GERA O HTML ---
    with open(ARQUIVO_BASE, "r", encoding="utf-8") as f:
        html_base = f.read()

    # Substitui os marcadores do CLIMA
    html_final = html_base.replace("{{TEMPERATURA}}", str(temperatura))
    html_final = html_final.replace("{{CONDICAO_TEMPO}}", condicao)
    html_final = html_final.replace("{{ICONE_TEMPO}}", url_icone)

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"Sucesso! Painel de clima gerado para {CIDADE} com {temperatura}°C.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
    exit(1)
