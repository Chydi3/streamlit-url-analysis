import json
import os

DATA_FILE = "player_name.json"

# ------------------ Helper Functions ------------------
def save_username_to_file(username):
    with open(DATA_FILE, "w") as f:
        json.dump({"username": username}, f)

def load_username_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("username", "")
    return ""

