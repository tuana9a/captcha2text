import os
import requests

url = "http://localhost:8080/"

for root, dirs, files in os.walk("./samples/", topdown=False):
    for name in files:
        filepath = os.path.join(root, name)
        img = open(filepath, "rb")
        response = requests.post(url, files={"file": img})
        print(response.text)
