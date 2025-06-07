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

#  BBOX = "lamin=-27.333&lomin=-52.36&lamax=-16.19&lomax=-44.736"

# --- FASE 2: USAR O TOKEN PARA BUSCAR OS DADOS DOS AVIÕES ---
@app.route('/aircraft_data')
def get_aircraft_data():
    if not ACCESS_TOKEN:
        return jsonify({"error": "Falha na autenticação com a OpenSky. Verifique as credenciais."}), 500

    # Coordenadas da sua área de interesse (min lat, max lat, min lon, max lon)
    BBOX_VALUES = (-27.333, -16.19, -52.36, -44.736) # Exemplo, ajuste para sua área
    data_url = "https://opensky-network.org/api/states/all"
    
    params = {
        'lamin': BBOX_VALUES[0],
        'lamax': BBOX_VALUES[1],
        'lomin': BBOX_VALUES[2],
        'lomax': BBOX_VALUES[3]
    }
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    
    try:
        print("Buscando dados dos aviões com o Access Token...")
        response = requests.get(data_url, headers=headers, params=params)
        response.raise_for_status()
        
        raw_data = response.json()
        
        # --- ESTA É A PARTE CORRIGIDA ---
        aircraft_list = []
        # Verifica se a resposta contém a chave "states" e se ela não é nula
        if raw_data and 'states' in raw_data and raw_data['states']:
            for s in raw_data['states']:
                # Mapeia os dados da lista para um objeto mais legível
                aircraft_list.append({
                    'icao24': s[0],
                    'callsign': s[1].strip() if s[1] else 'N/A',
                    'origin_country': s[2],
                    'longitude': s[5], # Atenção: lon e lat podem vir em ordens diferentes dependendo da API
                    'latitude': s[6],
                    'baro_altitude': s[7],
                    'on_ground': s[8],
                    'velocity': s[9],
                    'true_track': s[10], # Direção
                    'vertical_rate': s[11]
                })
        
        # Agora estamos retornando a LISTA processada, que o JavaScript espera
        return jsonify(aircraft_list)

    except requests.exceptions.HTTPError as e:
        print(f"Erro ao buscar dados dos aviões: {e.response.status_code}")
        return jsonify({"error": str(e)}), e.response.status_code
    except Exception as e:
        print(f"Erro inesperado ao buscar dados: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)