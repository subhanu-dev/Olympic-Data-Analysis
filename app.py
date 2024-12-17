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


@st.cache_data
def get_medal_count(data):
    medal_count = (
        data.groupby("region")["Medal"].count().sort_values(ascending=False).head(10)
    )
    # Reset the index to convert the Series to a DataFrame
    medal_count = medal_count.reset_index()
    return medal_count


@st.cache_data
def get_country_data(data):
    medal_counts = df.groupby(["Year", "Team"])["Medal"].count().reset_index()
    top_countries = (
        medal_counts.groupby("Team")["Medal"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )
    top_countries_data = medal_counts[medal_counts["Team"].isin(top_countries)]
    return top_countries_data


###################################################################################################################################################


st.title("Olympic Data Analysis (1896 - 2016) 🏅")

st.markdown(
    "A Historical analysis of the world's largest sporting event over a span of 120 years. Full analysis notebook ➡️ [notebook](https://github.com/subhanu-dev/Olympic-Data-Analysis/blob/main/Olympic%20Data%20Analysis.ipynb)"
)


# loading the data
df = load_data("data/merged_df.csv")

# setting columns

col1, col2 = st.columns([2, 1])


############## filtering data and select box

filtered_data = preprocess_data(df)


with col1:
    col1_1, col1_2, col1_3 = st.columns(3)  # defining sub columns
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

    with col1_3:
        sum = filtered_data["Name"].nunique()
        st.metric(label="Number of Contestants", value=sum)

    ################### plotting map

    st.markdown("### Participating Regions")
    # Plotting the map with the filtered data

    st.map(filtered_data[["latitude", "longitude"]])

    ############## plotting the bar graph of top countries
    medal_count = get_medal_count(filtered_data)

    sns.set_theme(style="whitegrid")

    # Creating the map
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x="region", y="Medal", data=medal_count, palette="viridis", ax=ax)
    plt.xlabel("Countries")
    plt.ylabel("Number of Medals")
    plt.xticks(rotation=45)

    st.subheader("Top 10 Countries Winning Medals")
    st.pyplot(fig)
    st.markdown("<br>", unsafe_allow_html=True)
    medal_count.index = range(1, len(medal_count) + 1)
    st.dataframe(medal_count.T)


with col2:
    ##############age distribution
    st.subheader("Age Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title("Athletes Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Number")

    # Plot using seaborn
    sns.histplot(
        data=filtered_data,
        x="Age",
        bins=np.arange(10, 80, 2),
        color="#099e50",
        edgecolor="red",
    )

    # Show the plot in Streamlit
    st.pyplot(fig)

    ######gender distribution
    st.subheader("Gender Distribution")
    fig, ax = plt.subplots(figsize=(6, 6))
    filtered_data["Sex"].value_counts().plot(
        kind="pie",
        autopct="%1.2f%%",
        ax=ax,
        colors=["#ffa04c", "#099e50"],
        shadow=True,
        explode=(0.05, 0.1),
    )

    # Displaying top athletes in the history of olympics
    top_athletes = (
        df.groupby(["Name", "Sex"])["Medal"]
        .count()
        .sort_values(ascending=False)
        .reset_index()
        .head(10)  # Select the top 10
    )

    ax.set_ylabel("")  # Hiding the y-axis label
    st.pyplot(fig)
    # Rename columns for better display
    top_athletes.columns = ["Athlete Name", "Sex", "Medal Count"]
    st.subheader("Top 10 Athletes by Medal Count")
    top_athletes.index = range(1, len(top_athletes) + 1)
    st.dataframe(top_athletes)

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Top 10 Countries' Olympic Performance - Against Time ")
# Add a slider to the sidebar:
selected_years = st.slider("Select a range of years", 1896, 2016, (2000, 2016))
top_countries_data = get_country_data(df)
specified_data = top_countries_data[
    top_countries_data["Year"].between(selected_years[0], selected_years[1])
]

fig, ax = plt.subplots(figsize=(18, 4))
sns.lineplot(
    data=specified_data,
    x="Year",
    y="Medal",
    hue="Team",
    ax=ax,
)

plt.xlabel("Year")
plt.ylabel("Number of Medals")
plt.legend(fontsize=10, loc="upper right")
st.pyplot(plt)


########################################################################################################


st.markdown("---")
st.markdown("Made with ❤️ by  [Subhanu](https://github.com/subhanu-dev)")
