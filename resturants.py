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

all_widgets = sp.create_widgets(df, create_data)
res = sp.filter_df(df, all_widgets)
st.title("Streamlit AutoPandas")
st.header("Original DataFrame")
st.write(df)

st.header("Result DataFrame")
st.write(res)

# Parse coordinates column into separate 'lat' and 'lon' columns
res[['lat', 'lon']] = res['coordinates'].str.split(',', expand=True).astype(float)

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
