from flask import Flask, request, jsonify
import datetime
import database # Importa o módulo do banco de dados simulado

app = Flask(__name__)

# Inicializa o banco de dados simulado
database.init_db()

@app.route("/api/occupancy", methods=["POST"])
def receive_occupancy_data():
    data = request.get_json()
    if not data or "mac_addresses" not in data:
        return jsonify({"error": "Invalid data. \"mac_addresses\" field is required."}), 400

    mac_addresses = data["mac_addresses"]
    timestamp = datetime.datetime.now().isoformat()
    unique_devices = len(set(mac_addresses)) # Contagem de dispositivos únicos

    occupancy_record = {
        "timestamp": timestamp,
        "mac_addresses": mac_addresses,
        "unique_devices": unique_devices
    }
    database.insert_occupancy_record(occupancy_record) # Insere no banco de dados simulado

    print(f"Received occupancy data: {occupancy_record}")

    return jsonify({"message": "Occupancy data received successfully", "unique_devices": unique_devices}), 200

@app.route("/api/occupancy", methods=["GET"])
def get_occupancy_data():
    return jsonify(database.get_all_occupancy_records()), 200 # Retorna dados do banco de dados simulado

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
