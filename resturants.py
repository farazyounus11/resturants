import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import pydeck as pdk

@st.cache_data
def load_data():
    df = pd.read_csv(file)
    return df

file = "data2.csv"
df = load_data()

df = df.drop_duplicates(keep='first')

create_data = {"categories": "text", "name": "text"}

all_widgets = sp.create_widgets(df, create_data)
res = sp.filter_df(df, all_widgets)
st.title("Streamlit AutoPandas")
st.header("Original DataFrame")
st.write(df)

st.header("Result DataFrame")
st.write(res)

# Parse coordinates data
def parse_coordinates(coordinates):
    try:
        coordinates = eval(coordinates)  # Evaluate string as dictionary
        latitude = coordinates['latitude']
        longitude = coordinates['longitude']
        return latitude, longitude
    except Exception as e:
        st.error(f"Error parsing coordinates: {e}")
        return None, None

# Apply parse_coordinates function to 'coordinates' column
res['lat'], res['lon'] = zip(*res['coordinates'].apply(parse_coordinates))

# Filter out rows with missing or invalid coordinates
res = res.dropna(subset=['lat', 'lon'])

# Plot the filtered data with PyDeck
st.header("Plotting with PyDeck")

# Example scatter plot
st.subheader("Scatter Plot")
scatterplot = pdk.Layer(
    "ScatterplotLayer",
    data=res,  # Use filtered DataFrame 'res' here
    get_position="[lon, lat]",
    get_radius=34,  # Adjust the radius to make the dots smaller
    get_fill_color=[255, 0, 0],
    pickable=True,
    auto_highlight=True,
)

# Set the initial view state latitude and longitude to NYC
view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=12, bearing=0, pitch=0)

tooltip = {
    "text": "Name: {name}\nReview Count: {review_count}\nCategories: {categories}\nRating: {rating}\nPrice: {price}\nLocation: {location}"
}

r = pdk.Deck(
    layers=[scatterplot],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v9",
    tooltip=tooltip,
)

st.pydeck_chart(r)
