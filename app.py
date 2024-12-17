import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="Olympic Data Analysis",  # setting page title and favicon
    page_icon="🏅",
    layout="wide",  # setting it to display in the wide layout
)


@st.cache_data  # making the data cached so we don't load the dataset all the time.
def load_data(filepath):
    return pd.read_csv(filepath)


@st.cache_data
def preprocess_data(data):
    # Rename columns and drop missing lat/lon rows
    data = data.rename(
        columns={"Latitude": "latitude", "Longitude": "longitude"}
    )  # Streamlit requires the latitude column to have specific names like LAT, LATITUDE, lat, or latitude
    data = data.dropna(
        subset=["latitude", "longitude"]
    )  # removes rows from the DataFrame df where the values in the columns "latitude" or "longitude" are NaN (missing).
    return data


################################################################


st.title("Olympic Data Analysis (1896 - 2016) 🏅")

st.markdown(
    "A Historical analysis of the world's largest sporting event over a span of 120 years"
)

df = load_data("data/merged_df.csv")

########Map


filtered_data = preprocess_data(df)

year = st.sidebar.selectbox("Select Year", sorted(filtered_data["Year"].unique()))
filtered_data = filtered_data[filtered_data["Year"] == year]

# Plot the filtered data
st.map(filtered_data[["latitude", "longitude"]])


######


st.selectbox(options=["today", "tomorrow"], label="subhanu")

if st.checkbox("Show dataframe"):
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    chart_data

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))


left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button("Press me!")

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        "Sorting hat", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write(f"You are in {chosen} house!")


########################################################################################################

# Displaying top athletes in the history of olympics
top_athletes = (
    df.groupby(["Name", "Sex"])["Medal"]
    .count()
    .sort_values(ascending=False)
    .reset_index()
    .head(10)  # Select the top 10
)

# Rename columns for better display
top_athletes.columns = ["Athlete Name", "Sex", "Medal Count"]
st.subheader("Top 10 Athletes by Medal Count")


col1, col2 = st.columns(2)  # Create two columns for side-by-side layout

with col1:
    st.pyplot(fig1)
with col2:
    st.table(top_athletes)
