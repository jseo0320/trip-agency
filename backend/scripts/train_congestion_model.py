import argparse
import pandas as pd
from app.ai.congestion.trainer import train

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--output",default="app/ai/congestion/model.joblib")
    args = parser.parse_args()
    train(pd.read_csv(args.csv),args.output)

if __name__ == "__main__":
    main()
