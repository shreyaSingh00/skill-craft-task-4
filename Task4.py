import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

# Step 1: Load the data
file_path = r'C:\Users\singh\OneDrive\Desktop\skill craft task\accidents.csv'
df = pd.read_csv(file_path)

# Step 2: Clean the data
# Convert 'Accident Date' to datetime format
df['Accident Date'] = pd.to_datetime(df['Accident Date'], format='%d/%m/%Y')
df['Year'] = df['Accident Date'].dt.year

# Convert 'Time (24hr)' to hour
df['Hour'] = df['Time (24hr)'] // 100

# Drop rows with missing 'Grid Ref: Easting' or 'Grid Ref: Northing'
df.dropna(subset=['Grid Ref: Easting', 'Grid Ref: Northing'], inplace=True)

# Step 3: Exploratory Data Analysis (EDA)
# Basic statistics
print(df.describe())

# Visualize the distribution of road surface, weather conditions, and time of day
fig, axs = plt.subplots(3, 1, figsize=(12, 15))

sns.countplot(data=df, x='Road Surface', ax=axs[0])
axs[0].set_title('Distribution of Road Surfaces')
axs[0].set_xlabel('Road Surface')
axs[0].set_ylabel('Count')

sns.countplot(data=df, x='Weather Conditions', ax=axs[1])
axs[1].set_title('Distribution of Weather Conditions')
axs[1].set_xlabel('Weather Conditions')
axs[1].set_ylabel('Count')

sns.histplot(data=df, x='Hour', bins=24, kde=True, ax=axs[2])
axs[2].set_title('Distribution of Accidents by Hour of Day')
axs[2].set_xlabel('Hour of Day')
axs[2].set_ylabel('Count')

plt.tight_layout()
plt.show()

# Step 4: Analyze Patterns
# Cross-tabulation of road surface and weather conditions
road_weather_crosstab = pd.crosstab(df['Road Surface'], df['Weather Conditions'])
print(road_weather_crosstab)

# Visualize the crosstab
plt.figure(figsize=(10, 6))
sns.heatmap(road_weather_crosstab, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Road Surface vs. Weather Conditions')
plt.xlabel('Weather Conditions')
plt.ylabel('Road Surface')
plt.show()

# Step 5: Visualize Accident Hotspots
# Convert easting and northing to latitude and longitude (approximation)
# These conversion steps may need to be adjusted based on the coordinate system used
df['latitude'] = df['Grid Ref: Northing'] * 0.00001
df['longitude'] = df['Grid Ref: Easting'] * 0.00001

# Create a map centered at the mean latitude and longitude
map_center = [df['latitude'].mean(), df['longitude'].mean()]
accident_map = folium.Map(location=map_center, zoom_start=10)

# Add heatmap layer
heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(accident_map)

# Save the map to an HTML file
accident_map.save('accident_hotspots.html')

# Step 6: Identify Contributing Factors
# Analyze the impact of road surface and weather on casualty severity
severity_road_surface = pd.crosstab(df['Road Surface'], df['Casualty Severity'])
severity_weather_conditions = pd.crosstab(df['Weather Conditions'], df['Casualty Severity'])

# Visualize the impact of road surface on casualty severity
plt.figure(figsize=(10, 6))
sns.heatmap(severity_road_surface, annot=True, fmt='d', cmap='OrRd')
plt.title('Road Surface vs. Casualty Severity')
plt.xlabel('Casualty Severity')
plt.ylabel('Road Surface')
plt.show()

# Visualize the impact of weather on casualty severity
plt.figure(figsize=(10, 6))
sns.heatmap(severity_weather_conditions, annot=True, fmt='d', cmap='OrRd')
plt.title('Weather Conditions vs. Casualty Severity')
plt.xlabel('Casualty Severity')
plt.ylabel('Weather Conditions')
plt.show()
