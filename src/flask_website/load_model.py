import pickle
from pathlib import Path

# Correct the variable to use __file__ with double underscores
model_path = Path(__file__).resolve().parent / 'final_xgb_model.pkl'

# Load the model and store it in a function
def load_xgb_model():
    with open(model_path, 'rb') as f:
        xgb_model = pickle.load(f)
    return xgb_model