"""
Super_ML.py

Supervised Machine Learning stage:
CSV -> features/target -> Random Forest Regressor -> Super_ML.joblib

Target:
    temperature_c

Features:
    humidity_percent
    pressure_hpa
    visibility_km
    wind_speed_mps
    cloudiness_percent
    latitude
    longitude
"""

from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

BASE_DIR=Path(__file__).resolve().parent
CSV_FILE=BASE_DIR/"weather_data.csv"
MODEL_FILE=BASE_DIR/"Super_ML.joblib"

FEATURES=[
    "humidity_percent","pressure_hpa","visibility_km",
    "wind_speed_mps","cloudiness_percent","latitude","longitude"
]
TARGET="temperature_c"

df=pd.read_csv(CSV_FILE)

missing=[c for c in FEATURES+[TARGET] if c not in df.columns]
if missing:
    raise ValueError(f"CSV is missing columns: {missing}")

df=df.dropna(subset=FEATURES+[TARGET]).copy()

if len(df)<5:
    raise ValueError("At least 5 valid rows are required to train the model.")

X=df[FEATURES]
y=df[TARGET]

model=RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    min_samples_leaf=1
)
model.fit(X,y)

joblib.dump(model,MODEL_FILE)

print("Supervised ML training completed.")
print(f"Rows used: {len(df)}")
print("Algorithm: Random Forest Regressor")
print("Target: temperature_c")
print(f"Saved model: {MODEL_FILE.name}")
