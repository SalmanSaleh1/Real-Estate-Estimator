# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 04:59:57 2024

@author: Yazeed Asim Alramadi

"""
import pandas as pd
import json

# File paths
json_file_path = r"C:\Users\moasl\Downloads\TestPrint.json"
csv_file_path = r"C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1_cleeaned30_2022.csv"

# Load JSON data
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

# Extract 'features' and convert to DataFrame
features = json_data['features']
json_df = pd.json_normalize(features)

# Preprocess JSON Data
json_df['properties.DISTRICT_NAME_D'] = json_df['properties.DISTRICT_NAME_D'].str.replace(r'^حي\s+', '', regex=True)
json_df['properties.CITY_NAME'] = json_df['properties.CITY_NAME'].str.replace('بريدة', 'بريده')

# Load CSV data
csv_df = pd.read_csv(csv_file_path)

# Preprocess CSV columns if necessary
csv_df['district'] = csv_df['district'].str.replace(r'^حي\s+', '', regex=True)
csv_df['city'] = csv_df['city'].str.replace('بريدة', 'بريده')

# Merge DataFrames based on matching columns
merged_df = pd.merge(
    json_df,
    csv_df,
    left_on=['properties.CITY_NAME', 'properties.DISTRICT_NAME_D', 'properties.SUBDIV_NO'],
    right_on=['city', 'district', 'Mukatat'],
    how='left'  # Keep all JSON rows, even if no match is found
)

# Add new columns to JSON with empty strings for no matches
merged_df['properties.property_type'] = merged_df['property_type'].fillna('')
merged_df['properties.Price_per_square_meter'] = merged_df['Price_per_square_meter'].fillna('')

# Handle cases where Mukatat and district = "أخرى" or Mukatat contains "حي/أخرى" and district is "أخرى"
other_condition = (
    ((csv_df['district'] == "أخرى") & (csv_df['Mukatat'] == "أخرى")) |
    (csv_df['Mukatat'].str.contains("حي/أخرى", na=False) & (csv_df['district'] == "أخرى"))
)

# Subset CSV for rows meeting the "other" condition
other_rows = csv_df[other_condition]

# Iterate through rows with the "other" condition to find matches based on PARCEL_NO
for index, row in other_rows.iterrows():
    parcel_no_matches = json_df['properties.PARCEL_NO'] == row['piece_num']
    json_df.loc[parcel_no_matches, 'properties.property_type'] = row['property_type']
    json_df.loc[parcel_no_matches, 'properties.Price_per_square_meter'] = row['Price_per_square_meter']

# Ensure missing values are replaced with empty strings
json_df['properties.property_type'] = json_df['properties.property_type'].fillna('')
json_df['properties.Price_per_square_meter'] = json_df['properties.Price_per_square_meter'].fillna('')

# Convert the updated DataFrame back to JSON format
updated_features = json_df.to_dict(orient='records')
updated_json_data = {'type': json_data['type'], 'features': updated_features}

# Save the updated JSON data back to a file
updated_json_file_path = r"C:\Users\moasl\Downloads\Updated_TestPrint.json"
with open(updated_json_file_path, 'w', encoding='utf-8') as updated_json_file:
    json.dump(updated_json_data, updated_json_file, ensure_ascii=False, indent=2)

print(f"Updated JSON file saved to {updated_json_file_path}")



import json

# File path
file_path = r"C:\Users\moasl\Downloads\Updated_TestPrint.json"

# Load the JSON file
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Add 'properties.area' attribute to all features
for feature in data.get('features', []):
    # Add the 'properties.area' key-value pair
    feature['properties.area'] = "منطقة القصيم"

# Save the updated JSON back to the file
output_path = r"C:\Users\moasl\Downloads\NEW.json"
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated JSON saved to {output_path}")






import pandas as pd
import json
import numpy as np
from catboost import CatBoostRegressor, Pool

# File paths
json_file_path = r"C:\Users\moasl\Downloads\NEW.json"
model_path = r"C:\Users\moasl\.spyder-py3\PJ\final_catboost_property_model_tunedNov5_925.cbm"
output_path = r"C:\Users\moasl\Downloads\Updated_TestPrint_with_ESTIMATED_PRICE.json"

# Load the JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract features from JSON for prediction
features_list = []
for i, feature in enumerate(data.get('features', [])):
    properties = feature  # JSON keys are directly prefixed with 'properties.'
    features_list.append({
        'area': properties.get('properties.area', 'unknown'),
        'CITY_NAME': properties.get('properties.CITY_NAME', 'unknown'),
        'DISTRICT_NAME_D': properties.get('properties.DISTRICT_NAME_D', 'unknown'),
        'SUBDIV_NO': properties.get('properties.SUBDIV_NO', 'unknown'),
        'PARCEL_LANDUSE': properties.get('properties.PARCEL_LANDUSE', 'unknown'),
        'property_type': properties.get('properties.property_type', 'unknown'),
        'Price_per_square_meter': properties.get('properties.Price_per_square_meter', 0),  # Default to 0 if missing
        'space': properties.get('properties.SHAPE.AREA', 0)  # Default to 0 if missing
    })

# Convert to DataFrame
features_df = pd.DataFrame(features_list)

# Rename columns to match model's expected features
features_df.rename(columns={
    'CITY_NAME': 'city',
    'DISTRICT_NAME_D': 'district',
    'SUBDIV_NO': 'Mukatat',
    'PARCEL_LANDUSE': 'property_classification'
}, inplace=True)

# Define categorical and numerical columns
categorical_columns = ['area', 'city', 'district', 'Mukatat', 'property_classification', 'property_type', 'Price_per_square_meter']
numerical_columns = ['space']

# Convert categorical columns to strings
for col in categorical_columns:
    features_df[col] = features_df[col].fillna('').astype(str)

# Ensure numerical columns are floats
for col in numerical_columns:
    features_df[col] = pd.to_numeric(features_df[col], errors='coerce').fillna(0).astype(float)

# Derive log_space from space
features_df['log_space'] = np.log1p(features_df['space'])  # log(1 + space)

# Load the pretrained model
model = CatBoostRegressor()
model.load_model(model_path)

# Check and align predict_df columns with model's expected features
print("Model expected features:", model.feature_names_)
print("Categorical features in model:", model.get_cat_feature_indices())
for feature in model.feature_names_:
    if feature not in features_df.columns:
        print(f"Missing feature: {feature}")
        raise ValueError(f"Feature {feature} is missing from the data!")

predict_df = features_df[model.feature_names_]

# Create a CatBoost Pool for prediction
cat_feature_indices = [predict_df.columns.get_loc(col) for col in categorical_columns]
prediction_pool = Pool(predict_df, cat_features=cat_feature_indices)

# Make predictions
log_predictions = model.predict(prediction_pool)
predicted_prices = np.expm1(log_predictions)  # Convert predictions back from log scale

# Add predictions into the JSON file with the correct key format
for i, feature in enumerate(data.get('features', [])):
    feature[f"properties.ESTIMATED_PRICE"] = float(predicted_prices[i])

# Save the updated JSON back to the file
with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated JSON with 'properties.ESTIMATED_PRICE' saved to {output_path}")




# Print district for every city
import pandas as pd

# File paths for the two CSV files
csv_file_path_1 = r"C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1_cleeaned30_2022.csv"
csv_file_path_2 = r"C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2022_q1.csv"

# Read both CSV files into DataFrames
df1 = pd.read_csv(csv_file_path_1)
df2 = pd.read_csv(csv_file_path_2)

# Define the columns to compare for uniqueness
compare_columns = ['city', 'district']  # Adjust these columns based on your files

# Ensure the relevant columns exist in both files
for col in compare_columns:
    if col not in df1.columns or col not in df2.columns:
        raise ValueError(f"Column '{col}' must exist in both CSV files.")

# Combine the two DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)

# Exclude rows where the district is 'أخرى' or 'حي/أخرى'
filtered_df = combined_df[~combined_df['district'].isin(['أخرى', 'حي/أخرى'])]

# Drop duplicates based on the compare_columns
unique_df = filtered_df.drop_duplicates(subset=compare_columns)

# Specify valid file paths
output_csv_path = r"C:\Users\moasl\Desktop\451\GPr\combined_unique.csv"
output_txt_path = r"C:\Users\moasl\Desktop\451\GPr\combined_unique.txt"

# Save the combined unique rows to a CSV file
unique_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
print(f"Combined unique rows saved to CSV at: {output_csv_path}")

# Save the combined unique rows to a text file
with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
    # Group districts by city
    city_district_mapping = unique_df.groupby('city')['district'].unique()
    for city, districts in city_district_mapping.items():
        txt_file.write(f"City: {city}\n")
        txt_file.write("Districts:\n")
        txt_file.write(", ".join(districts) + "\n")
        txt_file.write("-" * 40 + "\n")
print(f"Combined unique rows saved to text file at: {output_txt_path}")



import pandas as pd

# File paths for the two CSV files
csv_file_path_1 = r"C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1_cleeaned30_2022.csv"
csv_file_path_2 = r"C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2022_q1.csv"

# Read both CSV files into DataFrames
df1 = pd.read_csv(csv_file_path_1)
df2 = pd.read_csv(csv_file_path_2)

# Define relevant columns
required_columns = ['area', 'city', 'district', 'Mukatat']

# Ensure the relevant columns exist in both files
for col in required_columns:
    if col not in df1.columns or col not in df2.columns:
        raise ValueError(f"Column '{col}' must exist in both CSV files.")

# Combine the two DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)

# Exclude rows where the district or Mukatat is 'أخرى' or 'حي/أخرى'
filtered_df = combined_df[
    ~((combined_df['district'].isin(['أخرى', 'حي/أخرى'])) & (combined_df['Mukatat'] == 'أخرى'))
]

# Drop duplicates to ensure uniqueness
filtered_df = filtered_df.drop_duplicates(subset=required_columns)

# Group Mukatats by area, city, and district
output_txt_path = r"C:\Users\moasl\Desktop\451\GPr\area_city_district_mukatats.txt"
with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
    for area, area_group in filtered_df.groupby('area'):
        txt_file.write(f"Area: {area}\n")
        for city, city_group in area_group.groupby('city'):
            txt_file.write(f"\nCity: {city}\n")
            for district, district_group in city_group.groupby('district'):
                txt_file.write(f"\nDistrict: {district}\n")
                txt_file.write("Mukatats:\n")
                txt_file.write(", ".join(district_group['Mukatat'].unique()) + "\n")
                txt_file.write("===============\n")
            txt_file.write("-" * 40 + "\n")
print(f"Area, city, district, and Mukatats mapping saved to text file at: {output_txt_path}")





# Format Json file to rows
import json

def compact_json_format(input_file, output_file):
    """
    Converts a .json file to a compact JSON format with each feature on one line.
    
    Parameters:
    - input_file (str): Path to the input JSON file.
    - output_file (str): Path to save the compact JSON file.
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Validate the input structure
    if "type" not in data or data["type"] != "FeatureCollection" or "features" not in data:
        raise ValueError("Input JSON must be a valid FeatureCollection with features.")

    # Write the compact JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Convert each feature to a single line
        compact_features = []
        for feature in data["features"]:
            compact_features.append(json.dumps(feature, ensure_ascii=False))
        
        # Write the overall structure
        outfile.write('{\n')
        outfile.write('  "type": "FeatureCollection",\n')
        outfile.write('  "features": [\n')
        outfile.write(',\n'.join(compact_features))  # Join features with commas
        outfile.write('\n  ]\n')
        outfile.write('}\n')
    
    print(f"Compact JSON saved to {output_file}")

# Example usage
input_json = r"C:\Users\moasl\Downloads\filtered_file6.json"  # Replace with your JSON file path
output_json = r"C:\Users\moasl\Downloads\Formated_final.json"

compact_json_format(input_json, output_json)






import json

# Define the required attributes to check for emptiness
REQUIRED_ATTRIBUTES = [
    "area",
    "city_name",
    "district_name_d",
    "shape_area",
    "subdiv_no",
    "parcel_land_use",
    "property_type",
    "Price_per_square_meter"
]

def filter_json(input_file, output_file):
    try:
        # Read the input JSON file
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Ensure it's a valid GeoJSON with a "features" list
        if "features" not in data or not isinstance(data["features"], list):
            print("Invalid JSON structure: Missing 'features' key.")
            return

        # Filter features based on required attributes
        filtered_features = []
        for feature in data["features"]:
            properties = feature.get("properties", {})
            # Keep the feature only if all required attributes are non-empty
            if all(str(properties.get(attr, "")).strip() for attr in REQUIRED_ATTRIBUTES):
                filtered_features.append(feature)

        # Update the JSON structure with filtered features
        data["features"] = filtered_features

        # Write the filtered JSON to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Filtered JSON saved to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the input file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

input_file = r"C:\Users\moasl\Downloads\a.json"  # Replace with your input JSON file path
output_file = r"C:\Users\moasl\Downloads\aa.json"  # Replace with your output JSON file path
# Execute the filtering function
filter_json(input_file, output_file)




import json

# File paths
input_file = r"C:\Users\moasl\Downloads\filtered_file5.json"  # Input file
output_file = r"C:\Users\moasl\Downloads\filtered_file6.json"  # Output file

# Load the JSON file
with open(input_file, encoding="utf-8") as file:
    data = json.load(file)

# Total number of features before filtering
total_features = len(data["features"])

# Filter out records where "properties.DISTRICT_NAME_D" is empty
filtered_features = [
    feature for feature in data["features"]
    if feature.get("properties.Price_per_square_meter", "").float() != ""
]

# Total number of features after filtering
filtered_count = len(filtered_features)

# Calculate number of records removed
removed_count = total_features - filtered_count

# Update the original data dictionary
data["features"] = filtered_features

# Save the filtered data to a new JSON file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Print results
print(f"Filtered data saved to '{output_file}'.")
print(f"Total records before filtering: {total_features}")
print(f"Total records after filtering: {filtered_count}")
print(f"Total records removed: {removed_count}")





import json

# File paths
input_file = r"C:\Users\moasl\Downloads\filtered_file5.json"  # Input file
output_file = r"C:\Users\moasl\Downloads\filtered_file6.json"  # Output file

# Load the JSON file
with open(input_file, encoding="utf-8") as file:
    data = json.load(file)

# Attributes to remove
attributes_to_remove = [
    "properties.NOTES",
    "properties.CONSTRUCTION_TYPE",
    "properties.SPLIT_TYPE"
]

# Remove specified attributes from all features
for feature in data["features"]:
    for attr in attributes_to_remove:
        if attr in feature:
            del feature[attr]

# Save the updated data to a new JSON file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Print results
print(f"Attributes {attributes_to_remove} removed and updated data saved to '{output_file}'.")




import json

def txt_to_json_with_area(input_txt_path, output_json_path):
    """
    Convert area-city-district-Mukatat data in a text file to a JSON dictionary format.

    Parameters:
    - input_txt_path: Path to the input text file.
    - output_json_path: Path to save the JSON file.
    """
    with open(input_txt_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    area_city_mapping = {}
    current_area = None
    current_city = None

    for line in lines:
        line = line.strip()
        if line.startswith("Area:"):
            current_area = line.split("Area:")[1].strip()
            area_city_mapping[current_area] = {}
        elif line.startswith("City:"):
            current_city = line.split("City:")[1].strip()
            area_city_mapping[current_area][current_city] = {}
        elif line.startswith("District:"):
            current_district = line.split("District:")[1].strip()
            area_city_mapping[current_area][current_city][current_district] = []
        elif line and not line.startswith("=") and not line.startswith("-"):
            mukatats = [m.strip() for m in line.split(",")]
            area_city_mapping[current_area][current_city][current_district].extend(mukatats)

    # Save to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(area_city_mapping, json_file, ensure_ascii=False, indent=2)

    print(f"JSON file saved at: {output_json_path}")

# Example usage
input_txt_path = r"C:\Users\moasl\Desktop\451\GPr\city_district_mukatats.txt"

output_json_path = r"C:\Users\moasl\Desktop\451\GPr\city_district_mukatats_with_area.json"

txt_to_json_with_area(input_txt_path, output_json_path)


import json

def txt_to_json_with_area(input_txt_path, output_json_path):
    """
    Convert area-city-district-Mukatat data in a text file to a JSON dictionary format.
    
    Parameters:
    - input_txt_path: Path to the input text file.
    - output_json_path: Path to save the JSON file.
    """
    with open(input_txt_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()
    
    area_city_mapping = {}
    current_area = None
    current_city = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("Area:"):
            current_area = line.split("Area:")[1].strip()
            if current_area not in area_city_mapping:
                area_city_mapping[current_area] = {}
        elif line.startswith("City:"):
            if current_area is None:
                raise ValueError("City found without an associated Area in the input file.")
            current_city = line.split("City:")[1].strip()
            if current_city not in area_city_mapping[current_area]:
                area_city_mapping[current_area][current_city] = {}
        elif line.startswith("District:"):
            if current_city is None:
                raise ValueError("District found without an associated City in the input file.")
            current_district = line.split("District:")[1].strip()
            if current_district not in area_city_mapping[current_area][current_city]:
                area_city_mapping[current_area][current_city][current_district] = []
        elif line and not line.startswith("=") and not line.startswith("-"):
            if current_area is None or current_city is None:
                raise ValueError("Mukatats found without an associated Area or City in the input file.")
            mukatats = [m.strip() for m in line.split(",")]
            area_city_mapping[current_area][current_city][current_district].extend(mukatats)
    
    # Save to JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(area_city_mapping, json_file, ensure_ascii=False, indent=2)
    
    print(f"JSON file saved at: {output_json_path}")

# Example usage
input_txt_path = r"C:\Users\moasl\Desktop\451\GPr\area_city_district_mukatats.txt"
output_json_path = r"C:\Users\moasl\Desktop\451\GPr\city_district_mukatats_with_area.json"

txt_to_json_with_area(input_txt_path, output_json_path)














# Reformat Final JSON file

import json

# Load your JSON file
input_file =  r"C:\Users\moasl\Downloads\Formated_final.json"  # Replace with your input file name
output_file = r"C:\Users\moasl\Downloads\output.json"  # Replace with your output file name

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Transform the JSON
for feature in data["features"]:
    # Fix geometry structure
    geometry_type = feature.pop("geometry.type", None)
    geometry_coordinates = feature.pop("geometry.coordinates", None)
    feature["geometry"] = {
        "type": geometry_type,
        "coordinates": geometry_coordinates
    }
    
    # Move properties to a nested dictionary
    properties = {k.split(".")[-1]: v for k, v in feature.items() if "properties." in k}
    feature["properties"] = properties
    
    # Remove the old properties from the top level
    keys_to_remove = [k for k in feature.keys() if "properties." in k]
    for key in keys_to_remove:
        del feature[key]

# Save the transformed JSON to a new file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"Transformed JSON saved to {output_file}")


# Adding SHAPE.AREA to AREA
import json

# Load the JSON file
input_file = r"C:\Users\moasl\Downloads\output.json"  # Replace with your input file name
output_file = r"C:\Users\moasl\Downloads\output2.json"  # Replace with your output file name

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Modify the JSON
for feature in data["features"]:
    properties = feature.get("properties", {})
    # If 'AREA' exists, rename it to 'SHAPE.AREA'
    if "AREA" in properties:
        properties["SHAPE.AREA"] = properties.pop("AREA")

# Save the updated JSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print(f"Updated JSON saved to {output_file}")

import json

# Load the JSON file
input_file = r"C:\Users\moasl\Downloads\output2.json"   # Replace with your input file name
output_file = r"C:\Users\moasl\Downloads\Formated_final.json"  # Replace with your output file name

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Open the output file
with open(output_file, "w", encoding="utf-8") as file:
    # Write the initial part of the FeatureCollection
    file.write('{"type": "FeatureCollection", "features": [\n')
    
    # Write each feature on a single line
    for i, feature in enumerate(data["features"]):
        json.dump(feature, file, ensure_ascii=False)
        # Add a comma except for the last feature
        if i < len(data["features"]) - 1:
            file.write(",\n")
    file.write("\n]}")  # Close the FeatureCollection

print(f"Minified JSON saved to {output_file}")



