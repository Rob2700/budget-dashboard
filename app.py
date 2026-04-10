import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("💰 Budget Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Date Filter
df["date"] = pd.to_datetime(df["date"])
df["date"] = df["date"].dt.date

start_date = st.date_input("Start Date", df["date"].min())
end_date = st.date_input("End Date", df["date"].max())

df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]


# Filter
category = st.selectbox("Select Category", ["All"] + list(df["category"].unique()))

if category != "All":
    df = df[df["category"] == category]

# Show data
st.subheader("Transaction Data")
st.write(df)

# Total spending
total = df["amount"].sum()

# Spending by category
category_totals = df.groupby("category")["amount"].sum()

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Spending")
    st.metric(label="Total", value=f"${total}")

with col2:
    st.subheader("Entries")
    st.metric(label="Transactions", value=len(df))

# Bar chart
st.subheader("Spending by Category")
st.bar_chart(category_totals)

# Spacer
st.markdown("---")

# Pie chart

fig, ax = plt.subplots(facecolor='none')

wedges, texts, autotexts = ax.pie(
    category_totals,
    labels=category_totals.index,
    autopct="%1.1f%%"
    
)

#Force text to white
for text in texts:
    text.set_color("white")

for autotext in autotexts:
    autotext.set_color("white")

ax.set_facecolor('none')
ax.set_title("Spending Distribution", color="white")

st.pyplot(fig)