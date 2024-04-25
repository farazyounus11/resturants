import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import pydeck as pdk

@st.cache_data
def load_data():
    df = pd.read_csv(file)
    return df

file = "data1.csv"
df = load_data()

df = df.drop_duplicates(keep='first')

create_data = {"categories": "text", "name": "text"}

all_widgets = sp.create_widgets(df, create_data, ignore_columns=["Coordinates", "Price", "Display_Phone"])
res = sp.filter_df(df, all_widgets)
st.title("Streamlit AutoPandas")
st.header("Original DataFrame")
st.write(df)

st.header("Result DataFrame")
st.write(res)

# Check if the 'coordinates' column exists
if 'coordinates' in res.columns:
    coordinates_split = res['coordinates'].str.split(',', expand=True)
    
    # Check if the split resulted in two columns
    if len(coordinates_split.columns) == 2:
        # Try to convert the values to float
        try:
            res[['lat', 'lon']] = coordinates_split.astype(float)
        except ValueError as e:
            st.error(f"Error: Unable to convert coordinates to float values. Details: {e}")
            # Print out the problematic values for further investigation
            st.write("Problematic values in 'coordinates' column:")
            problematic_values = coordinates_split[~coordinates_split[0].astype(str).str.replace('.', '').str.isdigit() | ~coordinates_split[1].astype(str).str.replace('.', '').str.isdigit()]
            st.write(problematic_values)
    else:
        st.error("Error: The 'coordinates' column does not have the expected format.")
else:
    st.error("Error: The 'coordinates' column does not exist in the DataFrame.")

# Plot the filtered data with PyDeck
st.header("Plotting with PyDeck")

# Example scatter plot
st.subheader("Scatter Plot")
scatterplot = pdk.Layer(
    "ScatterplotLayer",
    data=res,  # Use filtered DataFrame 'res' here
    get_position="[lon, lat]",
    get_radius=200,
    get_fill_color=[255, 0, 0],
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=0, longitude=0, zoom=2, bearing=0, pitch=0)

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
