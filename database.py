import json

DATABASE_FILE = "simulated_database.json"

def init_db():
    try:
        with open(DATABASE_FILE, "r") as f:
            json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(DATABASE_FILE, "w") as f:
            json.dump({"occupancy_records": []}, f)
    print("Simulated database initialized.")

def insert_occupancy_record(record):
    with open(DATABASE_FILE, "r+") as f:
        data = json.load(f)
        data["occupancy_records"].append(record)
        f.seek(0)
        json.dump(data, f, indent=4)
    print(f"Record inserted into simulated database: {record}")

def get_all_occupancy_records():
    try:
        with open(DATABASE_FILE, "r") as f:
            data = json.load(f)
            return data.get("occupancy_records", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

if __name__ == "__main__":
    init_db()
    # Exemplo de uso
    # insert_occupancy_record({"timestamp": "2025-08-16T10:00:00", "unique_devices": 5})
    # print(get_all_occupancy_records())
