
import pandas as pd

# ==========================================
# STEP 32: POPULARITY GROWTH AND DECAY
# SPAIN TOP 50 SONGS
# ==========================================

# STEP 1: Load dataset

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

df["date"] = pd.to_datetime(df["date"])

df["popularity"] = pd.to_numeric(
    df["popularity"], errors="coerce"
)

# STEP 2: Remove missing popularity values

df = df.dropna(subset=["popularity"])

# STEP 3: Remove duplicate chart entries

df = df.drop_duplicates(
    subset=["date", "song", "artist"]
)

# STEP 4: Sort by date

df = df.sort_values("date")

# STEP 5: Calculate song popularity trends

popularity_analysis = df.groupby(
    ["song", "artist"]
).agg(
    first_date=("date", "min"),
    last_date=("date", "max"),
    initial_popularity=("popularity", "first"),
    final_popularity=("popularity", "last"),
    average_popularity=("popularity", "mean"),
    highest_popularity=("popularity", "max"),
    lowest_popularity=("popularity", "min"),
    chart_days=("date", "nunique")
).reset_index()

# STEP 6: Calculate popularity change

popularity_analysis["popularity_change"] = (
    popularity_analysis["final_popularity"] -
    popularity_analysis["initial_popularity"]
)

# STEP 7: Calculate growth percentage

popularity_analysis["growth_percentage"] = (
    popularity_analysis["popularity_change"] /
    popularity_analysis["initial_popularity"].replace(0, pd.NA)
) * 100

# STEP 8: Classify popularity trends

def classify_trend(change):

    if change > 0:
        return "Growing"

    elif change < 0:
        return "Declining"

    else:
        return "Stable"


popularity_analysis["popularity_trend"] = (
    popularity_analysis["popularity_change"]
    .apply(classify_trend)
)

# STEP 9: Sort by popularity growth

popularity_analysis = popularity_analysis.sort_values(
    by="popularity_change",
    ascending=False
)

# STEP 10: Display results

print("\n===== STEP 32: POPULARITY GROWTH AND DECAY =====")

print(
    popularity_analysis.head(20).to_string(index=False)
)

# STEP 11: Display trend summary

print("\n===== POPULARITY TREND SUMMARY =====")

print(
    popularity_analysis["popularity_trend"]
    .value_counts()
)

# STEP 12: Save report

popularity_analysis.to_csv(
    "Spain_Popularity_Growth_Decay_Analysis.csv",
    index=False
)

print("\nTotal songs analysed:",
      len(popularity_analysis))

print("\nPopularity growth and decay analysis completed!")

print("Report saved successfully!")
