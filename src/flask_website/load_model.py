from catboost import CatBoostRegressor
from pathlib import Path

# Define the path to the CatBoost model file
model_path = Path(__file__).resolve().parent / 'final_catboost_property_model_LATEST01.cbm'

# Load the CatBoost model
def load_catboost_model():
    model = CatBoostRegressor()
    model.load_model(str(model_path))
    return model
