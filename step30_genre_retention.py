
import pandas as pd

# ==========================================
# STEP 30: ALBUM TYPE-WISE RETENTION ANALYSIS
# SPAIN TOP 50 SONGS
# ==========================================

# STEP 1: Load dataset

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

print("\n===== STEP 30: ALBUM TYPE ANALYSIS =====")

# STEP 2: Convert date

df["date"] = pd.to_datetime(df["date"])

# STEP 3: Remove duplicate chart entries

df = df.drop_duplicates(
    subset=["date", "song", "artist"]
)

# STEP 4: Remove missing album types

df = df.dropna(subset=["album_type"])

# STEP 5: Calculate song-level retention

song_data = df.groupby(
    ["song", "artist", "album_type"]
).agg(
    chart_days=("date", "nunique"),
    first_date=("date", "min"),
    last_date=("date", "max")
).reset_index()

# STEP 6: Calculate lifespan

song_data["lifespan_days"] = (
    song_data["last_date"] -
    song_data["first_date"]
).dt.days + 1

# STEP 7: Calculate retention percentage

song_data["retention_rate"] = (
    song_data["chart_days"] /
    song_data["lifespan_days"]
) * 100

# STEP 8: Album type-wise comparison

album_analysis = song_data.groupby(
    "album_type"
).agg(
    total_songs=("song", "nunique"),
    average_chart_days=("chart_days", "mean"),
    average_lifespan=("lifespan_days", "mean"),
    average_retention=("retention_rate", "mean")
).reset_index()

# STEP 9: Sort results

album_analysis = album_analysis.sort_values(
    by="average_retention",
    ascending=False
)

# STEP 10: Display results

print("\n===== ALBUM TYPE RETENTION RESULTS =====")

print(album_analysis.to_string(index=False))

# STEP 11: Save report

album_analysis.to_csv(
    "Spain_Album_Type_Retention_Analysis.csv",
    index=False
)

print("\nTotal album types analysed:",
      len(album_analysis))

print("\nAlbum type retention analysis completed!")

print("Report saved successfully!")
