import requests

def query_lamb_v4(prompt: str) -> dict:
    response = requests.post("http://api.lamb_v4/predict", json={"prompt": prompt})
    return response.json()
