from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS # Certifique-se que flask_cors está instalado (pip install flask-cors)
import requests
import os

# --- INÍCIO DA SEÇÃO A SER VERIFICADA EM backend_app.py ---

# 1. Configurar a pasta estática:
app = Flask(__name__, static_folder='static') 

# 2. Habilitar CORS para a API (muito importante para comunicação cross-origin, mesmo que resolvamos o file://)
CORS(app) 

# Suas coordenadas de área de interesse (min_latitude, max_latitude, min_longitude, max_longitude)
# BOUNDING_BOX = "-10.0,-5.0,-40.0,-35.0" # Exemplo: Uma área abrangente na PB/RN. Adapte a sua!
# BOUNDING_BOX = "-23.612701, -23.637995,-46.654739,-46.674259" # São paulo/Rio de Janeiro
BOUNDING_BOX = "-16.19,-27.333,-52.36,-44.736" #-16.19, -52.36     -27.333, -44.736

@app.route('/aircraft_data')
def get_aircraft_data():
    url = f"https://opensky-network.org/api/states/all?lamin={BOUNDING_BOX.split(',')[0]}&lomin={BOUNDING_BOX.split(',')[2]}&lamax={BOUNDING_BOX.split(',')[1]}&lomax={BOUNDING_BOX.split(',')[3]}"
    print(f"Chamando OpenSky API com URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        print(f"Resposta bruta da OpenSky API: {raw_data}")
        
        aircraft_list = []
        if data and 'states' in data and data['states']:
            for s in data['states']:
                if s[5] is not None and s[6] is not None:
                    aircraft_list.append({
                        'icao24': s[0],
                        'callsign': s[1].strip() if s[1] else 'N/A',
                        'latitude': s[5], # OpenSky retorna lon, lat - o 5 é latitude, 6 é longitude (corrigido do exemplo anterior)
                        'longitude': s[6], # OpenSky retorna lon, lat
                        'true_track': s[10]
                    })
        return jsonify(aircraft_list)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# 3. Rota para servir o HTML (Geralmente na rota raiz '/')
@app.route('/')
def serve_map_html():
    return send_from_directory(app.static_folder, 'map_display.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000) # Garante que está na porta 5000