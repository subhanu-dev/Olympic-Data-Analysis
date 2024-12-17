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

# st.markdown(
#     "A Historical analysis of the world's largest sporting event over a span of 120 years"
# )

df = load_data("data/merged_df.csv")

# setting columns

col1, col2, col3 = st.columns([2, 1, 1])


############## filtering data and select box

filtered_data = preprocess_data(df)


with col1:
    col1_1, col1_2 = st.columns(2)  # defining sub columns
    with col1_1:
        year = st.selectbox(
            "Select Year",
            sorted(filtered_data["Year"].unique(), reverse=True),
            index=None,
        )

    # filtering data only if we select a specific year or else we have the entire dataset
    if year is not None:
        filtered_data = filtered_data[filtered_data["Year"] == year]

    with col1_2:
        regions = len(filtered_data["region"].unique())
        st.metric(label="Number of Countries", value=regions)

    ################### plotting map

    st.markdown("### Participating Regions")
    # Plotting the map with the filtered data

    st.map(filtered_data[["latitude", "longitude"]])

    medal_count = (
        filtered_data.groupby("region")["Medal"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    colors = [
        "#FF5733",
        "#C70039",
        "#900C3F",
        "#581845",
        "#FFC300",
        "#DAF7A6",
        "#33FF57",
        "#39C7C7",
        "#3357FF",
        "#FF33A8",
    ]

    # Create the plot
    fig, ax = plt.subplots()
    medal_count.plot(kind="bar", x="", y="Medal", color=colors, ax=ax)
    plt.xlabel("Countries")
    plt.ylabel("Number of Medals")
    plt.xticks(rotation=45)

    st.subheader("Top 10 Countries Winning Medals")
    st.pyplot(fig)


######gender distribution

with col2:
    st.subheader("Gender Distribution")
    fig, ax = plt.subplots(figsize=(4, 4))
    filtered_data["Sex"].value_counts().plot(
        kind="pie",
        autopct="%1.2f%%",
        ax=ax,
        colors=["#66b3ff", "#99ff99"],
        shadow=True,
        explode=(0.05, 0.1),
    )

    ax.set_ylabel("")  # Hide the y-axis label
    st.pyplot(fig)


st.selectbox(options=["today", "tomorrow"], label="subhanu")

if st.checkbox("Show dataframe"):
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    chart_data

# Add a selectbox to the sidebar:
add_selectbox = st.selectbox(
    "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
)

# Add a slider to the sidebar:
add_slider = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))


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

st.dataframe(top_athletes)

st.markdown("---")
st.markdown("Made with ❤️ by  [Subhanu](https://github.com/subhanu-dev)")
