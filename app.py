import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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

@app.route("/")
def home():
    return "API Flask rodando com Postgres no Heroku!"

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(name=data["name"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "name": new_user.name})

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

if __name__ == "__main__":
    # Cria tabelas automaticamente no primeiro run
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
