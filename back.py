# back.py
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Pega as credenciais do ambiente
CLIENT_ID = os.getenv('OPENSKY_USERNAME') # Usando a mesma variável do .env
CLIENT_SECRET = os.getenv('OPENSKY_PASSWORD') # Usando a mesma variável do .env

# print("--------DEBUG--------")
# print(f"CLIENT_ID: {CLIENT_ID}")
# print(f"CLIENT_SECRET: {CLIENT_SECRET}")
# print("---------------------")

# CLIENT_ID = "bingosky-api-client"
# CLIENT_SECRET = "fHJdTfcRExSpx10alZQ5YfaMWRG7Peex"


# --- FASE 1: FUNÇÃO PARA OBTER O TOKEN DE ACESSO ---
def get_opensky_token():
    """Pede um novo Access Token para a API de autenticação da OpenSky."""
    
    auth_url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        print("--- Obtendo novo Access Token da OpenSky ---")
        response = requests.post(auth_url, data=payload, headers=headers)
        response.raise_for_status()  # Lança um erro se a requisição falhar (ex: 401)
        
        token_data = response.json()
        access_token = token_data.get('access_token')
        
        if not access_token:
            print("ERRO: Access Token não encontrado na resposta.")
            return None
            
        print("--- Access Token obtido com sucesso! ---")
        return access_token

    except requests.exceptions.HTTPError as e:
        print(f"ERRO DE AUTENTICAÇÃO ao obter o token: {e.response.status_code}")
        print(f"Resposta do servidor: {e.response.text}")
        return None
    except Exception as e:
        print(f"ERRO inesperado ao obter o token: {e}")
        return None

# --- VARIÁVEL GLOBAL PARA ARMAZENAR O TOKEN ---
# Obtemos o token uma vez quando o servidor inicia.
# (Uma implementação mais avançada poderia verificar se o token expirou e pedir um novo)
ACCESS_TOKEN = get_opensky_token()

@app.route('/')
def serve_index():
    return send_from_directory('static', 'map_display.html')

# --- FASE 2: USAR O TOKEN PARA BUSCAR OS DADOS DOS AVIÕES ---
@app.route('/aircraft_data')
def get_aircraft_data():
    if not ACCESS_TOKEN:
        # Se não conseguimos o token na inicialização, retorna um erro.
        return jsonify({"error": "Falha na autenticação com a OpenSky. Verifique as credenciais."}), 500

    # Coordenadas da sua área de interesse (min lat, max lat, min lon, max lon)
    BBOX = "lamin=-27.333&lomin=-52.36&lamax=-16.19&lomax=-44.736" # Exemplo, ajuste para sua área
    data_url = f"https://opensky-network.org/api/states/all?{BBOX}"
    
    # O token é enviado no cabeçalho "Authorization" como um "Bearer Token"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    try:
        print("Buscando dados dos aviões com o Access Token...")
        response = requests.get(data_url, headers=headers)
        response.raise_for_status() # Lança erro para status 4xx/5xx
        
        data = response.json()
        # ... (processamento do JSON como fazíamos antes) ...
        return jsonify(data) # Apenas retornando o JSON bruto por enquanto

    except requests.exceptions.HTTPError as e:
        # Se o token expirou, poderíamos receber um 401 aqui.
        print(f"Erro ao buscar dados dos aviões: {e.response.status_code}")
        # Aqui poderíamos tentar obter um novo token, mas por enquanto vamos simplificar.
        return jsonify({"error": str(e)}), e.response.status_code
    except Exception as e:
        print(f"Erro inesperado ao buscar dados: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)