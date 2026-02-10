import librosa
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class SoundFeatureExtraction(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X_copy = X.copy()
        X_copy.columns = X_copy.columns.str.replace(" ", "_")
        sound_features = []
        features = {}

        for sound_file in X_copy["Heart_Sound_ID"]:

            sound, sample_rate = librosa.load(f"SoundsConcated/{sound_file}.wav")  ###

            zero_crossing_rate_mean = np.mean(librosa.feature.zero_crossing_rate(y=sound))
            zero_crossing_rate_std = np.std(librosa.feature.zero_crossing_rate(y=sound))
            spectral_centroid_mean = np.mean(librosa.feature.spectral_centroid(y=sound, sr=sample_rate))
            spectral_centroid_std = np.std(librosa.feature.spectral_centroid(y=sound, sr=sample_rate))

            mfcc = librosa.feature.mfcc(y=sound, sr=sample_rate, n_mfcc=20)
            delta = librosa.feature.delta(mfcc)
            delta2 = librosa.feature.delta(mfcc, order=2)

            features = {

                "zcr_mean": zero_crossing_rate_mean,
                "zcr_std": zero_crossing_rate_std,
                "spactral_centroid_mean": spectral_centroid_mean,
                "spactral_centroid_std": spectral_centroid_std

            }

            for i in range(20):
                features[f"mfcc_mean_{i}"] = np.mean(mfcc[i])
                features[f"mfcc_std_{i}"] = np.std(mfcc[i])
                features[f"delta_mean_{i}"] = np.mean(delta[i])
                features[f"delta2_mean_{i}"] = np.mean(delta2[i])

            sound_features.append(features)

        X_copy = X_copy.drop(columns="Heart_Sound_ID")
        X_features = pd.DataFrame(sound_features)

        X_final = pd.concat([X_copy, X_features], axis=1)

        return X_final


class LocationFeatureExtraction(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.mapping = {

            "Apex": "apex",
            "LC": "left,carotid",
            "LLSB": "left,lower,sternal_border",
            "LUSB": "left,upper,sternal_border",
            "RC": "right,carotid",
            "RUSB": "right,upper,sternal_border",
            'LUA': 'left,upper,anterior',  # New
            'RUA': 'right,upper,anterior',  # New
            'LMA': 'left,mid,anterior',  # New
            'RMA': 'right,mid,anterior',  # New
            'LLA': 'left,lower,anterior',  # New
            'RLA': 'right,lower,anterior'  # New
        }

        self.location_features = ["anterior", "apex", "carotid", "left", "lower", "mid", "right", "sternal_border",
                                  "upper"]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        dummies_mapping = X_copy["Location"].map(self.mapping)
        dummies_data = dummies_mapping.str.get_dummies(sep=",")

        dummies_data = dummies_data.reindex(columns=self.location_features, fill_value=0)

        X_copy = X_copy.drop(columns="Location")

        X_final = pd.concat([X_copy, dummies_data], axis=1)

        return X_final
