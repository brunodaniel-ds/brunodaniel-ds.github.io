import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Heroku já define DATABASE_URL como variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

# Ajuste necessário porque SQLAlchemy espera "postgresql://" e o Heroku fornece "postgres://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de exemplo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Modelo Occupancy (novo)
class Occupancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    mac_addresses = db.Column(db.JSON)
    unique_devices = db.Column(db.Integer)

@app.route("/")
def home():
    return "API Flask rodando com Postgres no Heroku!"

# Rotas Occupancy
@app.route("/api/occupancy", methods=["POST"])
def add_occupancy():
    data = request.get_json()
    if not data or "mac_addresses" not in data:
        return jsonify({"error": "Campo 'mac_addresses' obrigatório"}), 400

    record = Occupancy(
        mac_addresses=data["mac_addresses"],
        unique_devices=len(set(data["mac_addresses"]))
    )
    db.session.add(record)
    db.sessions.commit()

    return jsonify({
        "id": record.id,
        "timestamp": record.timestamp.isoformat(),
        "unique_devices": record.unique_devices
    }), 201

@app.route("/api/occupancy", methods=["GET"])
def get_occupancy():
    records = Occupancy.query.order_by(Occupancy.timestamp.asc()).all()
    return jsonify([
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat(),
            "mac_addresses": r.mac_addresses,
            "unique_devices": r.unique_devices
        } for r in records
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
