import pandas as pd
import numpy as np
import joblib
from extraction import SoundFeatureExtraction, LocationFeatureExtraction
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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

app.mount("/sounds", StaticFiles(directory=SOUND_DIR), name="sounds")

class HeartsFeatures(BaseModel):

    Gender: str
    Location: str
    Heart_Sound_ID: str = Field(alias="Heart Sound ID")

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
    file_path = f"{SOUND_DIR}/{sound_id}.wav"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Ses dosyası bulunamadı")

    try:

        sound, sample_rate = librosa.load(file_path, sr=None)


        if len(sound) > 0:
            max_val = np.max(np.abs(sound))
            if max_val > 0:
                boosted_sound = sound / max_val
            else:
                boosted_sound = sound
        else:
            boosted_sound = sound


        buffer = io.BytesIO()
        sf.write(buffer, boosted_sound, sample_rate, format='WAV')
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ses işleme hatası: {str(e)}")


@app.post("/predict")
async def predict(features: HeartsFeatures):

    input_data = features.model_dump(by_alias=True)
    input_data = pd.DataFrame([input_data])

    disease_prediction = encoder.inverse_transform(model.predict(input_data))[0]


    return {

        "prediction" : disease_prediction,
        "sound_id": features.Heart_Sound_ID

            }

