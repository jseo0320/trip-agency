from pathlib import Path
import joblib
import pandas as pd
from app.ai.congestion.preprocessing import prepare_features

class CongestionPredictor:
    def __init__(self, path: str = "app/ai/congestion/model.joblib") -> None:
        self.models = joblib.load(path) if Path(path).exists() else None

    def predict(self, frame: pd.DataFrame) -> dict[int,list[float]] | None:
        if self.models is None:
            return None
        features = prepare_features(frame)
        return {h: model.predict(features).clip(0,100).tolist() for h,model in self.models.items()}
