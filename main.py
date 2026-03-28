import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DeepL Yapılandırması
API_KEY = os.getenv("DEEPL_API_KEY")
URL = "https://api-free.deepl.com/v2/translate"

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

@app.post("/translate")
async def translate(request: TranslationRequest):
    try:
        # Yeni Güvenlik Kuralı: Anahtar artık Headers içinde gidiyor
        headers = {
            "Authorization": f"DeepL-Auth-Key {API_KEY}"
        }

        # Dil ayarlarını DeepL'in istediği formata getiriyoruz
        target = "EN-US" if request.target_lang.lower() == "en" else "TR"
        source = request.source_lang.upper()

        data = {
            "text": request.text,
            "target_lang": target,
            "source_lang": source
        }

        print(f"Güncel Yöntemle Gönderiliyor: {request.text}")

        # İsteği 'headers' parametresiyle beraber gönderiyoruz
        response = requests.post(URL, data=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return {"translated_text": result['translations'][0]['text']}
        else:
            return {"translated_text": f"DeepL Hatası ({response.status_code}): {response.text}"}
            
    except Exception as e:
        return {"translated_text": f"Sistem Hatası: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # Bazı sistemlerde localhost yerine 127.0.0.1 daha stabil çalışır
    uvicorn.run(app, host="127.0.0.1", port=8000)