import requests
from dotenv import load_dotenv
import os

load_dotenv(".env")
EMBEDDING_URL=os.getenv("EMBEDDING_URL")
CLOVA_STUDIO_API_KEY=os.getenv("CLOVA_STUDIO_API_KEY")
API_KEY_PRIMARY_VAL=os.getenv("API_KEY_PRIMARY_VAL")
REQUEST_ID=os.getenv("REQUEST_ID")
class EmbeddingService:

    def embedding(text:str):
        data = {"text": text}
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': CLOVA_STUDIO_API_KEY,
            'X-NCP-APIGW-API-KEY': API_KEY_PRIMARY_VAL,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': REQUEST_ID
        }

        response = requests.post(EMBEDDING_URL, headers=headers, json=data)

        result = response.json()
        if result.get('status', {}).get('code') == '20000':
            embedding = result.get('result', {}).get('embedding')
            print(embedding)
        else:
            return False
        return embedding