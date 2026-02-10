🧑🏼‍💻 To use the application: https://huggingface.co/spaces/berkaybln/HeartGuard 🧑🏼‍💻

❤️ Heart Disease Prediction from Heart Sounds

This project is an end-to-end Machine Learning solution that predicts the presence of heart disease by analyzing heart sounds. 
The project includes feature extraction from raw sound data, model training, and Dockerization of this model as an API.

🚀 Key Features

**Sound Analysis:** Features are extracted from sound files using the `Librosa` library.
**ML Model:** A high-accuracy classifier trained to recognize complex patterns in heart sounds.
**Modern Backend:** An asynchronous and fast API architecture with FastAPI.
**Dockerized:** Guaranteed seamless operation in any environment (Containerization).
**Frontend Ready:** Can integrate with a modern interface developed with Next.js.

🛠️ Technologies Used

**Language:** Python
**ML & Data Analysis:** Scikit-learn, Pandas, Numpy
**Audio Processing:** Librosa
**API Framework:** FastAPI, Uvicorn
**Deployment:** Docker

📂 Project Structure

main.py: API endpoints and application logic.

extraction.py: Functions for extracting features from audio files.

/SoundsConcated: Audio data used for model training and testing.

model_preparation.ipynb: Data discovery and model training process.

Dockerfile: Application packaging instructions.

📝 License

This project was developed for educational purposes.


ℹ️ For more information about the dataset used in model training:

https://archive.ics.uci.edu/dataset/1202/hls-cmds:+heart+and+lung+sounds+dataset+recorded+from+a+clinical+manikin+using+digital+stethoscope
