import pandas as pd

CSV_FILE = "user.csv"

def read_users():
    try:
        return pd.read_csv("user.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["username", "password", "name"])

def write_user(username, password, name):
    users = read_users()
    new_user = pd.DataFrame({"username": [username], "password": [password], "name": [name]})
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv("user.csv", index=False))
