from catboost import CatBoostRegressor
from pathlib import Path

# Define the path to the CatBoost model file
model_path = Path(__file__).resolve().parent / 'catboost_model.cbm'

# Load the CatBoost model
def load_catboost_model():
    model = CatBoostRegressor()
    model.load_model(str(model_path))
    return model
