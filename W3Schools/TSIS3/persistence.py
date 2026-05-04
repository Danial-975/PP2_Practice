import json

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

def load_settings():
    default = {"sound": True, "difficulty": "Medium"}
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return default

def load_data(filename, default):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score, distance):
    lb = load_data("leaderboard.json", [])
    lb.append({"name": name, "score": int(score), "distance": int(distance)})
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    save_data("leaderboard.json", lb)