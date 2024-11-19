# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 04:59:57 2024

@author: Yazeed Asim Alramadi

"""
# Importing necessary libraries
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the CSV file into a DataFrame
df1 = pd.read_csv(r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1.csv')


df2 = df1.copy()

df2 = df2.dropna(subset=['price', 'space'])

# Apply log transformation
df2['log_price'] = np.log1p(df2['price'])
df2['log_space'] = np.log1p(df2['space'])

# Filter based on max price threshold and drop remaining NaN values
df2 = df2[df2['log_price'] <= np.log1p(5000000)]
df2 = df2.dropna()

# Drop unnecessary columns
df2 = df2.drop(['ref_num', 'number_of_properties', 'price', 'piece_num'], axis='columns')

# Display the cleaned DataFrame
print("Number of rows after all cleaning steps:", df2.shape[0])

# Define features and target
X = df2.drop(['log_price'], axis=1)
y = df2['log_price']

# Specify categorical columns
categorical_columns = ['area', 'city', 'district', 'Mukatat', 'property_classification', 'property_type', 'Price_per_square_meter']
for col in categorical_columns:
    X[col] = X[col].astype(str)

# Load the pretrained model
model_path = r'C:\Users\moasl\final_catboost_property_model_nov18.cbm'
existing_model = CatBoostRegressor()
existing_model.load_model(model_path)

# Continue training the model with the cleaned data
existing_model.fit(
    X,
    y,
    cat_features=categorical_columns,
    init_model=existing_model,  # Continue training from the loaded model
    verbose=100
)

# Save the updated model
existing_model.save_model('catboost_property_model_updated_with_more_data_nov18.cbm')

# Optional: Evaluate model performance
y_pred_log = existing_model.predict(X)
y_pred = np.expm1(y_pred_log)  # Convert predictions back to the original scale
y_original_scale = np.expm1(y)

mae = mean_absolute_error(y_original_scale, y_pred)
rmse = np.sqrt(mean_squared_error(y_original_scale, y_pred))
r2 = r2_score(y_original_scale, y_pred)

print(f"MAE on Extended Data: {mae}")
print(f"RMSE on Extended Data: {rmse}")
print(f"R-squared on Extended Data: {r2}")

