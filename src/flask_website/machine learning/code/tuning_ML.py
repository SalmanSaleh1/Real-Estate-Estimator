# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 04:59:57 2024

@author: Yazeed Asim Alramadi

"""
## Manual

from catboost import Pool
import numpy as np
import pandas as pd

# Define the prediction function with dynamic column ordering and transformation for 'log_space'
def predict_property_value(area, city, district, Mukatat, space, property_classification, property_type, Price_per_square_meter=None):
    # Construct the input data
    input_data = pd.DataFrame({
        'area': [str(area)],
        'city': [str(city)],
        'district': [str(district)],
        'Mukatat': [str(Mukatat)],
        'space': [space],  # Numeric value
        'log_space': [np.log1p(space)],  # Log-transformed space value
        'property_classification': [str(property_classification)],
        'property_type': [str(property_type)],
        'Price_per_square_meter': [str(Price_per_square_meter) if Price_per_square_meter is not None else 'unknown']
    })
    
    # Ensure column order matches model's training features
    model_features = final_model.feature_names_
    input_data = input_data[model_features]  # Reorder columns based on model's feature order
    
    # Create a Pool object for prediction
    predict_pool = Pool(input_data, cat_features=categorical_columns)
    
    # Predict log price and convert back to original scale
    log_price_pred = final_model.predict(predict_pool)
    predicted_price = np.expm1(log_price_pred)
    
    return predicted_price[0]

# Example manual test
manual_prediction = predict_property_value(
    area="منطقة الرياض",
    city="الرياض",
    district="الزهرة",
    Mukatat="1017",
    space=400.0,
    property_classification="سكني",
    property_type="قطعة أرض",
    Price_per_square_meter=500
)
print(f"Predicted Property Value: {manual_prediction}")





## CSV

import pandas as pd
import numpy as np
from catboost import CatBoostRegressor, Pool

# Load the trained model
model_path = r'C:\Users\moasl\.spyder-py3\PJ\final_catboost_property_model_tunedNov5_925.cbm'
model = CatBoostRegressor()
model.load_model(model_path)

# Define categorical columns as they were during training
categorical_columns = ['area', 'city', 'district', 'Mukatat', 'property_classification', 'property_type', 'Price_per_square_meter']

# Define the function to predict from a CSV file
def predict_from_csv(input_csv_path, output_csv_path):
    # Load the data
    data = pd.read_csv(input_csv_path)
    
    # Check if 'space' column exists and apply log transformation
    if 'space' in data.columns:
        data['log_space'] = np.log1p(data['space'])
    else:
        # Assign a default value for 'log_space' if 'space' is missing
        print("'space' column not found. Assigning a default value for 'log_space'.")
        data['log_space'] = np.log1p(400)  # Default space, adjust based on typical values
    
    # Convert categorical columns to strings to match training configuration
    for col in categorical_columns:
        if col in data.columns:
            data[col] = data[col].astype(str)
        else:
            data[col] = 'unknown'  # Placeholder if the column is missing

    # Ensure column order matches the model's training features
    model_features = model.feature_names_
    data = data[model_features]  # Reorder columns to match model's feature order
    
    # Create a Pool object with specified categorical features
    predict_pool = Pool(data, cat_features=categorical_columns)
    
    # Generate predictions
    log_price_predictions = model.predict(predict_pool)
    data['predicted_value'] = np.expm1(log_price_predictions)  # Convert from log scale
    
    # Save the results with predictions to a new CSV
    data.to_csv(output_csv_path, index=False)
    print(f"Predictions saved to {output_csv_path}")

# Example usage
input_csv_path = r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1_cleeaned30_2022.csv'  # Replace with your actual input CSV file
output_csv_path = 'predicted_property_values.csv'
predict_from_csv(input_csv_path, output_csv_path)






#######################################################################
#######################################################################

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Assuming y_combined and y_pred_combined are the true and predicted values
mae_combined = mean_absolute_error(y_combined_original_scale, y_pred_combined)
rmse_combined = np.sqrt(mean_squared_error(y_combined_original_scale, y_pred_combined))
r2_combined = r2_score(y_combined_original_scale, y_pred_combined)

print(f"Mean Absolute Error (MAE): {mae_combined}")
print(f"Root Mean Squared Error (RMSE): {rmse_combined}")
print(f"R-squared (R²): {r2_combined}")


#######################################################################
#######################################################################

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_combined_original_scale, y_pred_combined, alpha=0.5)
plt.plot([y_combined_original_scale.min(), y_combined_original_scale.max()], 
         [y_combined_original_scale.min(), y_combined_original_scale.max()], 'r--')  # Ideal line
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Predicted vs. Actual Property Prices")
plt.show()


residuals = y_combined_original_scale - y_pred_combined
plt.figure(figsize=(8, 6))
plt.hist(residuals, bins=30, alpha=0.7, color='blue')
plt.xlabel("Residuals")
plt.ylabel("Frequency")
plt.title("Distribution of Residuals")
plt.show()


#######################################################################
#######################################################################

import time

start_time = time.time()
y_pred_combined = final_model.predict(X_combined)  # Adjust based on your model's predict function
end_time = time.time()

response_time = (end_time - start_time) / len(X_combined)  # Average time per prediction
print("Average Prediction Time:", response_time, "seconds per request")
