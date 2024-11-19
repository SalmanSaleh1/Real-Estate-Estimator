# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 04:59:57 2024

@author: Yazeed Asim Alramadi

"""

#Plot
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV

# Set plotting parameters
%matplotlib inline
import matplotlib
matplotlib.rcParams["figure.figsize"] = (20,10)

# Load the CSV file into a DataFrame
df1 = pd.read_csv(r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2022_q1.csv')

# Plotting the distribution of property prices
plt.figure(figsize=(12, 6))
plt.hist(df1['price'], bins=30, color='blue', alpha=0.7)
plt.xlabel('Property Prices (SAR)')
plt.ylabel('Frequency')
plt.title('Distribution of Property Prices')

# Adjust x-axis labels for better formatting
ticks = np.arange(0, 2_100_000, 200_000)  # Set ticks from 0 to 2,000,000 with steps of 200,000
labels = [f"{int(tick/1_000_000)}M" if tick >= 1_000_000 else f"{int(tick/1_000)}K" for tick in ticks]
plt.xticks(ticks=ticks, labels=labels, rotation=45)  # Rotate for better spacing

plt.tight_layout()  # Ensure no overlap or clipping
plt.savefig('property_price_distribution_fixed.png')
plt.show()



import pandas as pd
import matplotlib.pyplot as plt
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# Read the CSV files
file_2022 = r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2022_q1.csv'
file_2023 = r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1_cleeaned30_2022.csv'

# Load the data
data_2022 = pd.read_csv(file_2022)
data_2023 = pd.read_csv(file_2023)

# Ensure consistent column names
data_2022.columns = [col.strip().lower() for col in data_2022.columns]
data_2023.columns = [col.strip().lower() for col in data_2023.columns]

# Function to process and plot data
def plot_top_counts(data, group_col, title, xlabel, ylabel, n=5):
    # Group by the specified column and count occurrences
    counts = data.groupby(group_col).size().reset_index(name='count')
    # Sort by count and select the top n
    top_counts = counts.sort_values(by='count', ascending=False).head(n)
    # Reshape and fix Arabic text
    top_counts[group_col] = top_counts[group_col].apply(lambda x: get_display(reshape(x)))
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(top_counts[group_col], top_counts['count'], color='purple', alpha=0.8)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.show()

# Plot for 2022 Q1 - Top 5 Areas
plot_top_counts(
    data_2022,
    group_col='area',
    title='Top 5 Areas with Most Properties (2022 Q1)',
    xlabel='Area',
    ylabel='Number of Properties'
)

# Plot for 2022 Q1 - Top 5 Cities
plot_top_counts(
    data_2022,
    group_col='city',
    title='Top 5 Cities with Most Properties (2022 Q1)',
    xlabel='City',
    ylabel='Number of Properties'
)

# Plot for 2023 Q1 - Top 5 Areas
plot_top_counts(
    data_2023,
    group_col='area',
    title='Top 5 Areas with Most Properties (2023 Q1)',
    xlabel='Area',
    ylabel='Number of Properties'
)

# Plot for 2023 Q1 - Top 5 Cities
plot_top_counts(
    data_2023,
    group_col='city',
    title='Top 5 Cities with Most Properties (2023 Q1)',
    xlabel='City',
    ylabel='Number of Properties'
)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the 2022 Q1 dataset
file_2022 =  r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2022_q1.csv'
data_2022 = pd.read_csv(file_2022)

# Ensure consistent column names
data_2022.columns = [col.strip().lower() for col in data_2022.columns]

# Convert the 'price' column to numeric, if necessary
data_2022['price'] = pd.to_numeric(data_2022['price'], errors='coerce')

# Drop rows with missing or invalid prices
data_2022 = data_2022.dropna(subset=['price'])

# Extract the price column
price_data = data_2022['price']

# Plotting the price distribution (Histogram + KDE)
plt.figure(figsize=(10, 6))
sns.histplot(price_data, kde=True, bins=30, color='purple', alpha=0.8)
plt.title('Price Distribution for 2022 Q1', fontsize=14)
plt.xlabel('Price (SAR)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

# Adjust x-axis labels for better formatting
ticks = np.arange(0, price_data.max() + 200_000, 200_000)  # Set ticks with steps of 200,000
labels = [f"{int(tick/1_000_000)}M" if tick >= 1_000_000 else f"{int(tick/1_000)}K" for tick in ticks]
plt.xticks(ticks=ticks, labels=labels, rotation=45)  # Rotate for better spacing

plt.tight_layout()
plt.savefig('price_distribution_2022.png')
plt.show()

# Optional: Add a boxplot below the histogram
plt.figure(figsize=(10, 2))
sns.boxplot(x=price_data, color='purple')
plt.title('Price Spread for 2022 Q1', fontsize=12)
plt.xlabel('Price (SAR)', fontsize=10)

# Adjust x-axis labels for boxplot
plt.xticks(ticks=ticks, labels=labels, rotation=45)
plt.tight_layout()
plt.savefig('price_boxplot_2022.png')
plt.show()



# to get median average 
import pandas as pd

# Load the 2022 Q1 dataset
file_2022 =  r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2022_q1.csv'
data_2022 = pd.read_csv(file_2022)

# Ensure consistent column names
data_2022.columns = [col.strip().lower() for col in data_2022.columns]

# Convert the 'price' column to numeric, if necessary
data_2022['price'] = pd.to_numeric(data_2022['price'], errors='coerce')

# Drop rows with missing or invalid prices
data_2022 = data_2022.dropna(subset=['price'])

# Calculate the median price
median_price = data_2022['price'].median()

# Calculate the average price
average_price = data_2022['price'].mean()

# Determine the most expensive property type
most_expensive_property_type = data_2022.groupby('property_type')['price'].mean().idxmax()
most_expensive_price = data_2022.groupby('property_type')['price'].mean().max()

# Output the results
print(f"Median Price: {median_price:,.2f} SAR")
print(f"Average Price: {average_price:,.2f} SAR")
print(f"Most Expensive Property Type: {most_expensive_property_type} (Average Price: {most_expensive_price:,.2f} SAR)")




# for Property Types and Classifications
# Count the occurrences of each property type
property_type_counts = data_2022['property_type'].value_counts()

# Calculate the average price for each property type
property_type_avg_price = data_2022.groupby('property_type')['price'].mean()

# Count the occurrences of each property classification
property_classification_counts = data_2022['property_classification'].value_counts()

# Calculate the average price for each property classification
property_classification_avg_price = data_2022.groupby('property_classification')['price'].mean()

# Output results
print("Property Types:")
print(property_type_counts)
print("\nAverage Price by Property Type:")
print(property_type_avg_price)

print("\nProperty Classifications:")
print(property_classification_counts)
print("\nAverage Price by Property Classification:")
print(property_classification_avg_price)


# Plot for Property Types
import pandas as pd
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display

# Function to reshape and display Arabic text
def reshape_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# Apply reshaping to property types
property_type_counts.index = [reshape_arabic_text(x) for x in property_type_counts.index]

# Plot for Property Types
plt.figure(figsize=(8, 6))
property_type_counts.plot.pie(autopct='%1.1f%%', colors=['purple', 'orange', 'green'], startangle=90)
plt.title(reshape_arabic_text('Percentage of Property Types (2022 Q1)'), fontsize=14)
plt.ylabel('')
plt.tight_layout()
plt.savefig('property_types_2022.png')
plt.show()


# Plot for Property Classifications
# Apply reshaping to property classifications
property_classification_counts.index = [reshape_arabic_text(x) for x in property_classification_counts.index]

# Plot for Property Classifications
plt.figure(figsize=(8, 6))
property_classification_counts.plot.bar(color=['blue', 'red', 'green', 'purple'], alpha=0.7)
plt.title(reshape_arabic_text('Property Classifications (2022 Q1)'), fontsize=14)
plt.xlabel(reshape_arabic_text('Property Classifications'), fontsize=12)
plt.ylabel(reshape_arabic_text('Number of properties'), fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('property_classification_2022.png')
plt.show()



#get type of data
import pandas as pd

# Load your dataset
df = pd.read_csv(r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2022_q1.csv')  # Replace with the path to your dataset

# Display column names and their data types
print(df.dtypes)







import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1_cleeaned30_2022.csv'  # Update with your dataset path
df = pd.read_csv(file_path)

# Check for Missing Values
print("Missing Values Analysis:")
missing_values = df.isnull().sum() / len(df) * 100  # Percentage of missing values
print(missing_values)

# Visualization of Missing Values (only if missing values exist)
missing_values = missing_values[missing_values > 0]  # Filter columns with missing values
if not missing_values.empty:
    missing_values.plot(kind='bar', color='skyblue', figsize=(8, 5))
    plt.title("Percentage of Missing Values by Column")
    plt.ylabel("Percentage")
    plt.xlabel("Columns")
    plt.tight_layout()
    plt.show()
else:
    print("No missing values found in the dataset.")

# Handling Missing Values
if 'price' in df.columns:
    df['price'] = df['price'].fillna(df['price'].median())  # Median imputation for 'price'
if 'district' in df.columns:
    df['district'] = df['district'].fillna('Unknown')  # Flag missing districts with 'Unknown'

# Visualize Outliers Using Box Plots
numeric_columns = ['price', 'Price_per_square_meter']  # Columns to check for outliers
for col in numeric_columns:
    if col in df.columns:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x=col)
        plt.title(f"Box Plot for {col}")
        plt.show()

# Identify and Handle Outliers
for col in numeric_columns:
    if col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1  # Interquartile range
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        print(f"\nOutlier Analysis for {col}:")
        print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
        print(f"Outliers Count: {((df[col] < lower_bound) | (df[col] > upper_bound)).sum()}")

        # Optionally Remove Outliers
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

# Check for Inconsistencies
if 'city' in df.columns:
    print("\nUnique Values in 'city':")
    print(df['city'].unique())
    
# Remove outliers
df = df[(df['price'] <= 1392850) & (df['price'] > 0)]
df = df[(df['Price_per_square_meter'] <= 2487.85) & (df['Price_per_square_meter'] > 0)]

df.to_csv(r'C:\Users\moasl\Desktop\451\GPr\cleaned_realestate_2023_q1_cleeaned30_2022_cleanedv2.csv', index=False)












