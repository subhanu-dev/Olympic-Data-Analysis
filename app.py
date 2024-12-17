import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("merged_df.csv")


st.set_page_config(
    page_title="Olympic Data Analysis",  # setting page title and favicon
    page_icon="🏅",
    layout="wide",  # setting it to display in the wide layout
)

st.title("Olympic Data Analysis (1896 - 2026)")

st.markdown("hi machn")

fig1, ax1 = plt.subplots(figsize=(6, 6))  # Specify plot size
df["Season"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", ax=ax1, colors=["#66b3ff", "#99ff99"]
)
ax1.set_title("Number of Contestants by Season")
ax1.set_ylabel("")

map_data = df["Latitudes", "Longitudes"]


st.map(map_data)

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
