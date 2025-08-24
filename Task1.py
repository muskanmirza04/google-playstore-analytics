import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ---------------------------
# Load dataset
# ---------------------------
# Apna dataset yaha read kar (file ka naam accordingly change karna)
df = pd.read_csv("apps.csv")

# ---------------------------
# Time Restriction (3PM - 5PM IST)
# ---------------------------
current_time = datetime.datetime.now().time()
if not (datetime.time(15, 0) <= current_time <= datetime.time(17, 0)):
    print("Graph is not available outside 3PM - 5PM IST window.")
    exit()

# ---------------------------
# Data Cleaning & Filtering
# ---------------------------

# Convert columns
df["Size"] = df["Size"].str.replace("M", "").astype(float)
df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")

# Filter conditions:
# 1. Average rating >= 4.0
# 2. Size >= 10 MB
# 3. Last update in January (any year)
df = df[(df["Rating"] >= 4.0) &
        (df["Size"] >= 10) &
        (df["Last Updated"].dt.month == 1)]

# ---------------------------
# Aggregate: Top 10 categories by installs
# ---------------------------
df["Installs"] = df["Installs"].str.replace("+", "").str.replace(",", "").astype(int)

category_group = df.groupby("Category").agg({
    "Rating": "mean",
    "Reviews": "sum",
    "Installs": "sum"
}).reset_index()

# Top 10 by installs
top10 = category_group.sort_values("Installs", ascending=False).head(10)

# ---------------------------
# Plot Grouped Bar Chart
# ---------------------------
x = range(len(top10))
width = 0.35

plt.figure(figsize=(12, 6))

# Bar for Ratings
plt.bar([p - width/2 for p in x], top10["Rating"], width=width, label="Average Rating")

# Bar for Reviews
plt.bar([p + width/2 for p in x], top10["Reviews"], width=width, label="Total Reviews")

plt.xticks(x, top10["Category"], rotation=45, ha="right")
plt.xlabel("App Categories")
plt.ylabel("Values")
plt.title("Average Rating vs Total Reviews for Top 10 Categories (Filtered)")
plt.legend()
plt.tight_layout()

# Save chart as image
plt.savefig("task1_output.png")
plt.show()
