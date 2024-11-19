# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 04:59:57 2024

@author: Yazeed Asim Alramadi

"""
# Import necessary libraries
import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
file_path = r'C:\Users\moasl\Desktop\451\GPr\RealEstate.csv'
df1 = pd.read_csv(file_path)

# Strip any leading or trailing spaces from column names
df1.columns = df1.columns.str.strip()

new_column_names = {
    'المنطقة': 'area', 
    'المدينة': 'city',
    'الحي': 'district',
    'تصنيف العقار': 'property_classification',
    'نوع العقار': 'property_type',
    'عدد العقارات': 'number_of_properties',
    'السعر بالريال السعودي': 'price',
    'المساحة': 'space',
    'سعر المتر المربع': 'Price_per_square_meter',
    'رقم مرجعي': 'ref_num',
    'المخطط': 'Mukatat',
    'رقم القطعة': 'piece_num',
    'التاريخ': 'date'  # Added this line to rename 'التاريخ' to 'date'
}

df1 = df1.rename(columns=new_column_names)

print("Columns in DataFrame after renaming:", df1.columns)

# Remove specific prefixes from 'district', 'Mukatat', and 'piece_num'
df1['district'] = df1['district'].str.replace(r'^حي/', '', regex=True)  # Remove "حي/"
df1['Mukatat'] = df1['Mukatat'].str.replace(r'^مخطط/', '', regex=True)  # Remove "مخطط/"
# Remove the prefix "قطعة " (with a space) from 'piece_num'
if 'piece_num' in df1.columns:
    # Strip spaces first, then replace the prefix
    df1['piece_num'] = df1['piece_num'].str.strip().str.replace(r'^قطعة ', '', regex=True)


# Verify the changes
print("\nSample updated district values:", df1['district'].head())
print("\nSample updated Mukatat values:", df1['Mukatat'].head())
print("\nSample updated piece_num values:", df1['piece_num'].head())


# Clean up specific columns
df1['price'] = pd.to_numeric(df1['price'].astype(str).str.replace(',', ''), errors='coerce')
df1['space'] = pd.to_numeric(df1['space'].astype(str).str.replace(',', ''), errors='coerce')
df1['Price_per_square_meter'] = pd.to_numeric(df1['Price_per_square_meter'].astype(str).str.replace(',', ''), errors='coerce')

# Drop rows with NaN values in critical columns
df1 = df1.dropna(subset=['price', 'space', 'Price_per_square_meter'])

# Replace infrequent districts with a placeholder
df1['district'] = df1['district'].apply(lambda x: x.strip() if isinstance(x, str) else x)
district_stats = df1['district'].value_counts(ascending=False)
district_stats_less_than_10 = district_stats[district_stats <= 10]
df1['district'] = df1['district'].apply(lambda x: 'حي/أخرى' if x in district_stats_less_than_10 else x)

# Function to remove outliers in specific columns
def remove_outliers(df, column_name):
    mean = df[column_name].mean()
    std_dev = df[column_name].std()
    return df[(df[column_name] > (mean - 2 * std_dev)) & (df[column_name] < (mean + 2 * std_dev))]

# Apply outlier removal
df1 = remove_outliers(df1, 'Price_per_square_meter')
df1 = remove_outliers(df1, 'price')
df1 = remove_outliers(df1, 'space')

# Additional filtering and cleaning
df1 = df1[df1['Price_per_square_meter'] <= 5000]
df1['Mukatat'] = df1['Mukatat'].str.replace(r'\s*/\s*', '/', regex=True)
df1 = df1[~((df1['Mukatat'] == "بدون") & (df1['piece_num'] == "بدون"))]

# Further processing
df1['price'] = pd.to_numeric(df1['price'], errors='coerce')
df1['space'] = pd.to_numeric(df1['space'], errors='coerce')

# Keep only specific property types
allowed_property_types = ["أرض", "شقة", "أرض زراعية"]
df1 = df1[df1['property_type'].isin(allowed_property_types)]

# Filter rows with number_of_properties > 1
df1 = df1[df1['number_of_properties'] <= 1]

# Save the cleaned DataFrame to a new CSV file
output_path = r'C:\Users\moasl\Desktop\451\GPr\n.csv'
df1.to_csv(output_path, index=False)

# Summary statistics and verification
print("File saved successfully to:", output_path)
print("\nSummary Statistics:")
print(df1.describe())

print("\nUnique property types:")
print(df1['property_type'].unique())

print("\nCity counts:")
print(df1['city'].value_counts())

print("\nDistrict counts:")
print(df1['district'].value_counts())

print("\nArea counts:")
print(df1['area'].value_counts())

