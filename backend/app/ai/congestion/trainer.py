from pathlib import Path
import joblib
import pandas as pd
from lightgbm import LGBMRegressor
from app.ai.congestion.preprocessing import prepare_features

def train(frame: pd.DataFrame, output: str) -> None:
    models = {}
    for hour in (1,2,3):
        target = f"future_congestion_{hour}h"
        rows = frame.dropna(subset=[target])
        model = LGBMRegressor(n_estimators=150, random_state=42)
        model.fit(prepare_features(rows), rows[target])
        models[hour] = model
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(models,output)
