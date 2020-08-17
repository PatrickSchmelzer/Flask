import os
import requests

def uploadFile():
    absolutePath = os.path.dirname(os.path.abspath(__file__))
    filePath = absolutePath + '\\test.txt'
    print(filePath)
    with open(filePath, 'rb') as f:
        requests.post('http://localhost:5000/upload', data=f)