# backend_app.py

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os  # Importe a biblioteca 'os'
from dotenv import load_dotenv  # Importe a função 'load_dotenv'
from flask import send_from_directory

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Pega as credenciais do ambiente
# A função os.getenv() lê as variáveis que carregamos com load_dotenv()
OPENSKY_USER = os.getenv('OPENSKY_USERNAME')
OPENSKY_PASS = os.getenv('OPENSKY_PASSWORD')

print(f"--- DEBUG ---")
print(f"Usuário carregado do .env: '{OPENSKY_USER}'")
print(f"Senha carregada do .env: '{OPENSKY_PASS}'")
print(f"-------------")

# Suas coordenadas
BOUNDING_BOX = "-27.333,-16.19,-52.36,-44.736" # lamax,lamin,lomax,lomin (invertido na sua pergunta anterior)
# Corrigindo a ordem para a URL: lamin,lamax,lomin,lomax
LAMIN, LAMAX, LOMIN, LOMAX = "-27.333" ,"-16.19" , "-52.36", "-44.736" # Note a inversão aqui para o URL estar correto
# A sua bounding box estava invertida (min > max). Corrigi para um exemplo válido sobre o Brasil.
# Exemplo para o sudeste do Brasil: LAMIN, LAMAX, LOMIN, LOMAX = "-25.0", "-22.0", "-48.0", "-42.0"

@app.route('/')
def serve_index():
    # Esta linha diz ao Flask para enviar o arquivo 'index.html'
    # que está no mesmo diretório que o script 'back.py'
    return send_from_directory('static', 'map_display.html')

@app.route('/aircraft_data')
def get_aircraft_data():
    url = f"https://opensky-network.org/api/states/all?lamin={LAMIN}&lomin={LOMIN}&lamax={LAMAX}&lomax={LOMAX}"
    
    try:
        print("Fazendo requisição autenticada para a OpenSky API...")
        
        # A biblioteca 'requests' usa o parâmetro 'auth' para fazer a autenticação HTTP Basic
        response = requests.get(url, auth=(OPENSKY_USER, OPENSKY_PASS), timeout=15)
        
        response.raise_for_status()
        data = response.json()
        
        aircraft_list = []
        if data and 'states' in data and data['states']:
            for s in data['states']:
                if s[5] is not None and s[6] is not None:
                    aircraft_list.append({
                        'icao24': s[0],
                        'callsign': s[1].strip() if s[1] else 'N/A',
                        'latitude': s[6],   # Corrigido: OpenSky retorna lon, lat
                        'longitude': s[5], # Corrigido: OpenSky retorna lon, lat
                        'true_track': s[10]
                    })
        return jsonify(aircraft_list)

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para a API OpenSky: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Ocorreu um erro inesperado no servidor: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True)