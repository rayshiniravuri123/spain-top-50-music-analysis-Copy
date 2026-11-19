
import pandas as pd

# ==========================================
# STEP 31: DURATION & ALBUM SIZE VS RETENTION
# SPAIN TOP 50 SONGS
# ==========================================

# STEP 1: Load dataset

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

df["date"] = pd.to_datetime(df["date"])

df["duration_ms"] = pd.to_numeric(
    df["duration_ms"], errors="coerce"
)

df["total_tracks"] = pd.to_numeric(
    df["total_tracks"], errors="coerce"
)

# STEP 2: Remove duplicate chart entries

df = df.drop_duplicates(
    subset=["date", "song", "artist"]
)

# STEP 3: Calculate song-level retention

song_data = df.groupby(
    ["song", "artist"]
).agg(
    chart_days=("date", "nunique"),
    first_date=("date", "min"),
    last_date=("date", "max"),
    duration_ms=("duration_ms", "median"),
    total_tracks=("total_tracks", "median")
).reset_index()

# STEP 4: Calculate lifespan

song_data["lifespan_days"] = (
    song_data["last_date"] -
    song_data["first_date"]
).dt.days + 1

# STEP 5: Calculate retention rate

song_data["retention_rate"] = (
    song_data["chart_days"] /
    song_data["lifespan_days"]
) * 100

# STEP 6: Convert duration into minutes

song_data["duration_minutes"] = (
    song_data["duration_ms"] / 60000
)

# STEP 7: Create duration categories

song_data["duration_category"] = pd.cut(
    song_data["duration_minutes"],
    bins=[0, 2.5, 3.5, 4.5, float("inf")],
    labels=[
        "Short (Under 2.5 min)",
        "Medium (2.5-3.5 min)",
        "Long (3.5-4.5 min)",
        "Very Long (Above 4.5 min)"
    ]
)

# STEP 8: Create album size categories

song_data["album_size_category"] = pd.cut(
    song_data["total_tracks"],
    bins=[0, 3, 7, 12, float("inf")],
    labels=[
        "Small (1-3 tracks)",
        "Medium (4-7 tracks)",
        "Large (8-12 tracks)",
        "Very Large (13+ tracks)"
    ]
)

# STEP 9: Duration-wise retention analysis

duration_analysis = song_data.groupby(
    "duration_category",
    observed=True
).agg(
    total_songs=("song", "nunique"),
    average_chart_days=("chart_days", "mean"),
    average_lifespan=("lifespan_days", "mean"),
    average_retention=("retention_rate", "mean")
).reset_index()

# STEP 10: Album-size retention analysis

album_analysis = song_data.groupby(
    "album_size_category",
    observed=True
).agg(
    total_songs=("song", "nunique"),
    average_chart_days=("chart_days", "mean"),
    average_lifespan=("lifespan_days", "mean"),
    average_retention=("retention_rate", "mean")
).reset_index()

# STEP 11: Display results

print("\n===== DURATION VS RETENTION =====")

print(duration_analysis.to_string(index=False))

print("\n===== ALBUM SIZE VS RETENTION =====")

print(album_analysis.to_string(index=False))

# STEP 12: Save reports

duration_analysis.to_csv(
    "Spain_Duration_Retention_Analysis.csv",
    index=False
)

album_analysis.to_csv(
    "Spain_Album_Size_Retention_Analysis.csv",
    index=False
)

song_data.to_csv(
    "Spain_Duration_Album_Retention_Details.csv",
    index=False
)

print("\n===== STEP 31 COMPLETED =====")

print("Duration report saved!")
print("Album size report saved!")
print("Detailed retention report saved!")
