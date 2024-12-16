import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df_athletes = pd.read_csv(r"./data/athlete_events.csv")
df_countries = pd.read_csv(r"./data/noc_regions.csv")
df = df_athletes.merge(df_countries, how="left", on="NOC")
df = df.drop_duplicates()
df = df.drop(columns={"notes"})


st.set_page_config(
    page_title="Olympic Data Analysis",  # setting page title and favicon
    page_icon="🏅",
)

st.title("Olympic Data Analysis (1896 - 1026)")

st.markdown("hi machn")

fig1, ax1 = plt.subplots(figsize=(6, 6))  # Specify plot size
df["Season"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", ax=ax1, colors=["#66b3ff", "#99ff99"]
)
ax1.set_title("Number of Contestants by Season")
ax1.set_ylabel("")


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
