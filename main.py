import pandas as pd
import numpy as np
import joblib
from extraction import SoundFeatureExtraction, LocationFeatureExtraction
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
import soundfile as sf
import librosa
import os
import io

import __main__
__main__.SoundFeatureExtraction = SoundFeatureExtraction
__main__.LocationFeatureExtraction = LocationFeatureExtraction

import sklearn
sklearn.set_config(transform_output="pandas")


model = joblib.load("model_heart_disease_prediction.pkl")
encoder = joblib.load("encoder_heart_disease_prediction.pkl")

SOUND_DIR = "SoundsConcated"

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


frontend_path = "frontend/out"
static_path = os.path.join(frontend_path, "static")
next_static_path = os.path.join(frontend_path, "_next/static")


if os.path.exists(next_static_path):
    app.mount("/_next/static", StaticFiles(directory=next_static_path), name="next-static")


if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
else:
    print("Uyarı: 'static' klasörü bulunamadı, ancak uygulama devam ediyor.")
    
app.mount("/sounds", StaticFiles(directory=SOUND_DIR), name="sounds")

NORMALIZED_DIR = "normalized_sounds"
os.makedirs(NORMALIZED_DIR, exist_ok=True)

app.mount("/normalized", StaticFiles(directory=NORMALIZED_DIR), name="normalized")



class HeartsFeatures(BaseModel):

    Gender: str
    Location: str
    Heart_Sound_ID: str = Field(alias="Heart Sound ID")


@app.get("/")
async def serve_frontend():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend dosyaları bulunamadı."}


@app.get("/get-sounds")
async def get_sounds():


    sounds = [f.replace(".wav", "") for f in os.listdir(SOUND_DIR) if f.endswith(".wav")]
    return {"sounds": sounds}




@app.get("/listen/{sound_id}")


async def listen_boosted_sound(sound_id: str):
    """
    Ses kayıtları ses şiddeti olarak oldukça düşük seviyede.
    Burada sesi normalize eder (sesini yükseltir) ve tarayıcıya stream olarak gönderir.
    """
    src_path = f"{SOUND_DIR}/{sound_id}.wav"
    out_path = f"{NORMALIZED_DIR}/{sound_id}.wav"

    if not os.path.exists(src_path):
        raise HTTPException(status_code=404)

    if not os.path.exists(out_path):
        sound, sr = librosa.load(src_path, sr=16000)
        max_val = np.max(np.abs(sound))
        if max_val > 0:
            sound = sound / max_val
        sf.write(out_path, sound, sr, subtype='PCM_16')

    return FileResponse(out_path, media_type="audio/wav")


@app.post("/predict")
async def predict(features: HeartsFeatures):

    input_data = features.model_dump(by_alias=True)
    input_data = pd.DataFrame([input_data])

    disease_prediction = encoder.inverse_transform(model.predict(input_data))[0]


    return {

        "prediction" : disease_prediction,
        "sound_id": features.Heart_Sound_ID

            }
