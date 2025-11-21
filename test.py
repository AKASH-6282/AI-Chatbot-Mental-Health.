import requests

msg = {"message": "I am feeling stressed"}
r = requests.post("http://127.0.0.1:5000/chat", json=msg)

print(r.json())
