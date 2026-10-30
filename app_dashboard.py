import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Global Video Game Sales Dashboard", layout="wide")
st.title("🎮 Global Video Game Sales Analytical Dashboard (1980 - 2020)")

@st.cache_data
def load_data():
    df = pd.read_csv("Video_Games_Sales_Dataset.csv")
    return df

df = load_data()

st.sidebar.header("Dashboard Filters")
platforms = st.sidebar.multiselect("Select Platform Type:", df["Platform.type"].unique(), default=df["Platform.type"].unique())
years = st.sidebar.slider("Select Release Year Range:", int(df["Year"].min()), int(df["Year"].max()), (1980, 2020))

filtered_df = df[(df["Platform.type"].isin(platforms)) & (df["Year"].between(years[0], years[1]))]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Titles Analyzed", f"{len(filtered_df):,}")
k2.metric("Total Global Sales", f"{filtered_df['Global_Sales'].sum():,.2f} M")
k3.metric("Top Genre", filtered_df.groupby("Genre")["Global_Sales"].sum().idxmax())
k4.metric("Top Platform Family", filtered_df.groupby("Platform.type")["Global_Sales"].sum().idxmax())

st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader("1. Global Video Game Sales Over Years")
    yearly = filtered_df.groupby("Year")["Global_Sales"].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(yearly["Year"], yearly["Global_Sales"], marker="o", color="darkgreen", label="global_sales")
    ax1.set_title("Global Video Game Sales Over Years")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Global Sales (millions)")
    ax1.grid(True)
    ax1.legend()
    st.pyplot(fig1)

with c2:
    st.subheader("2. Global Sales per Genre")
    genre_s = filtered_df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars = ax2.bar(genre_s["Genre"], genre_s["Global_Sales"], color="#1f77b4")
    ax2.set_title("Global Sales per Genre")
    ax2.set_xlabel("Genre")
    ax2.set_ylabel("Sales (in million)")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig2)

c3, c4 = st.columns(2)

with c3:
    st.subheader("3. Scatter Plot of European Sales vs. North American Sales")
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.regplot(data=filtered_df, x="NA_Sales", y="EU_Sales", ax=ax3, scatter_kws={"alpha":0.6}, line_kws={"color":"red"})
    ax3.set_title("Scatter Plot of European Sales vs. North American Sales with Trend Line")
    st.pyplot(fig3)

with c4:
    st.subheader("4. Global Sales (Log) by Platform & Rating Type")
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=filtered_df, x="Platform.type", y="Global.Sales.Log", hue="Rating.type", ax=ax4)
    ax4.set_title("Global Sales Log Distribution by Platform & Rating Type")
    st.pyplot(fig4)
