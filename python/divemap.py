import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load your CSV file containing dive data
dive_data = pd.read_csv('/Users/mitchtork/website/assets/files/DiveLog.csv')

# Calculate total number of dives and dive time
total_dive_count = dive_data['Dive #'].max()  # Assuming Dive # is a unique identifier for each dive
total_dive_time_minutes = dive_data['Dive Time (min)'].sum()
total_dive_time_hours = total_dive_time_minutes // 60
remaining_minutes = total_dive_time_minutes % 60

# Aggregate the data by location and count the number of dives
location_counts = dive_data.groupby(['Location', 'lat', 'lon']).size().reset_index(name='counts')

# Determine the maximum number of dives at any single location for color scaling
max_dives = location_counts['counts'].max()

# Create a base map, centering it on an area that will definitely be visible
map_dive_locations = folium.Map(location=[0, 0], zoom_start=2)

# Marker cluster
marker_cluster = MarkerCluster().add_to(map_dive_locations)

# Loop through the aggregated data and add each location as a marker on the map
for idx, row in location_counts.iterrows():
    color = f"#{int((1 - row['counts'] / max_dives) * 255):02x}0000ff"
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        popup=(
            f"<strong>Location:</strong> {row['Location']}<br>"
            f"<strong>Dives:</strong> {row['counts']}"
        ),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=row['counts'] / max_dives
    ).add_to(marker_cluster)

# Prepare the HTML for the dive stats, styled as a ticker
html = f"""
<div style="background-color: rgba(0,0,0,0.8); color: white; font-size:16px; padding:10px; border-radius: 8px; border: 2px solid #0078A8; position: absolute; top: 10px; left: 50%; transform: translateX(-50%); z-index:1000;">
    <strong>Dive Stats:</strong> {total_dive_count} Dives | {total_dive_time_hours}h {remaining_minutes}m Underwater
</div>
"""

# Add HTML to the map using a simple iframe embedded in a popup (alternative approach)
iframe = folium.IFrame(html=html, width=300, height=100)
popup = folium.Popup(iframe, max_width=300)
folium.Marker(location=[20, 0], popup=popup).add_to(map_dive_locations)

# Save the map to an HTML file
map_dive_locations.save('/Users/mitchtork/website/assets/files/DiveLog.html')
