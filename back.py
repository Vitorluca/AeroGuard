# app.py (exemplo básico com Flask)
from flask import Flask, jsonify
import requests

# app = Flask(__name__)
app = Flask(__name__, static_folder='static')

# Suas coordenadas de área de interesse (min_latitude, max_latitude, min_longitude, max_longitude)
BOUNDING_BOX = "LAT_MIN,LAT_MAX,LON_MIN,LON_MAX" # Substitua pelos seus valores

@app.route('/aircraft_data')
def get_aircraft_data():
    # Exemplo de chamada à API OpenSky para uma área
    # Use 'states/all' para buscar todos os estados de aeronaves.
    # Adicione bbox para filtrar pela sua área.
    # docs: https://opensky-network.org/apidoc/rest.html#all-states
    url = f"https://opensky-network.org/api/states/all?lamin={BOUNDING_BOX.split(',')[0]}&lomin={BOUNDING_BOX.split(',')[2]}&lamax={BOUNDING_BOX.split(',')[1]}&lomax={BOUNDING_BOX.split(',')[3]}"

    try:
        response = requests.get(url)
        response.raise_for_status() # Lança um erro para status de erro (4xx ou 5xx)
        data = response.json()

        # Opcional: Processar e formatar os dados aqui
        aircraft_list = []
        if data and 'states' in data and data['states']:
            for s in data['states']:
                # s[0]=icao24, s[1]=callsign, s[5]=latitude, s[6]=longitude, s[10]=true_track (heading)
                if s[5] is not None and s[6] is not None: # Apenas se tiver lat/lon
                    aircraft_list.append({
                        'icao24': s[0],
                        'callsign': s[1].strip() if s[1] else 'N/A',
                        'latitude': s[6], # OpenSky retorna lon, lat
                        'longitude': s[5], # OpenSky retorna lon, lat
                        'true_track': s[10] # Direção em graus
                    })
        return jsonify(aircraft_list)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Lembre-se de substituir BOUNDING_BOX
    # Ex: BOUNDING_BOX = "32.0,33.0,-80.0,-79.0"
    app.run(debug=True)