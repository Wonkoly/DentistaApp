import json

def load_users():
    with open("data/users.json", "r") as f:
        return json.load(f)

def login_user(email, password):
    users = load_users()
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user
    return None
