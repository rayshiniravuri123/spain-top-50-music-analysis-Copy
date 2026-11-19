
import pandas as pd

# ==========================================
# STEP 33: BUSINESS KPI CALCULATION
# SPAIN TOP 50 SONGS
# ATLANTIC RECORDING CORPORATION
# ==========================================

# STEP 1: Load dataset

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

df["date"] = pd.to_datetime(df["date"])

df["position"] = pd.to_numeric(
    df["position"], errors="coerce"
)

# STEP 2: Clean duplicate records

df = df.drop_duplicates(
    subset=["date", "song", "artist"]
)

# STEP 3: Calculate song-level metrics

song_data = df.groupby(
    ["song", "artist"]
).agg(
    chart_days=("date", "nunique"),
    first_date=("date", "min"),
    last_date=("date", "max"),
    best_position=("position", "min"),
    album_type=("album_type", "first"),
    is_explicit=("is_explicit", "first")
).reset_index()

# STEP 4: Calculate song lifespan

song_data["lifespan_days"] = (
    song_data["last_date"] -
    song_data["first_date"]
).dt.days + 1

# STEP 5: Calculate retention stability

song_data["retention_rate"] = (
    song_data["chart_days"] /
    song_data["lifespan_days"]
) * 100

# STEP 6: Calculate entry-to-peak time

peak_dates = (
    df.sort_values("position")
    .groupby(["song", "artist"])
    .first()
    .reset_index()[["song", "artist", "date"]]
    .rename(columns={"date": "peak_date"})
)

song_data = song_data.merge(
    peak_dates,
    on=["song", "artist"],
    how="left"
)

song_data["entry_to_peak_days"] = (
    song_data["peak_date"] -
    song_data["first_date"]
).dt.days

# STEP 7: Calculate playlist churn rate

daily_entries = df.groupby("date").agg(
    daily_songs=("song", "count")
)

first_appearances = (
    df.groupby(["song", "artist"])["date"]
    .min()
    .reset_index()
)

daily_new_entries = (
    first_appearances.groupby("date")
    .size()
)

daily_new_entries = daily_new_entries.reindex(
    daily_entries.index,
    fill_value=0
)

playlist_churn_rate = (
    daily_new_entries.mean() /
    daily_entries["daily_songs"].mean()
) * 100

# STEP 8: Calculate explicit content score

df["is_explicit"] = (
    df["is_explicit"]
    .astype(str)
    .str.lower()
    .str.strip()
)

song_data["is_explicit"] = (
    song_data["is_explicit"]
    .astype(str)
    .str.lower()
    .str.strip()
)

explicit_days = song_data.loc[
    song_data["is_explicit"].isin(["true", "1"]),
    "chart_days"
].mean()

clean_days = song_data.loc[
    song_data["is_explicit"].isin(["false", "0"]),
    "chart_days"
].mean()

if pd.notna(clean_days) and clean_days > 0:
    explicit_lifecycle_score = (
        explicit_days / clean_days
    ) * 100
else:
    explicit_lifecycle_score = float("nan")

# STEP 9: Calculate Single vs Album ratio

song_data["album_type"] = (
    song_data["album_type"]
    .astype(str)
    .str.lower()
    .str.strip()
)

single_days = song_data.loc[
    song_data["album_type"] == "single",
    "chart_days"
].mean()

album_days = song_data.loc[
    song_data["album_type"] == "album",
    "chart_days"
].mean()

if pd.notna(album_days) and album_days > 0:
    single_album_ratio = single_days / album_days
else:
    single_album_ratio = float("nan")

# STEP 10: Calculate all six KPIs

kpis = pd.DataFrame({
    "KPI": [
        "Average Days on Playlist",
        "Entry-to-Peak Time",
        "Playlist Churn Rate",
        "Retention Stability Index",
        "Explicit Content Lifecycle Score",
        "Single vs Album Longevity Ratio"
    ],

    "Value": [
        song_data["chart_days"].mean(),
        song_data["entry_to_peak_days"].mean(),
        playlist_churn_rate,
        song_data["retention_rate"].mean(),
        explicit_lifecycle_score,
        single_album_ratio
    ],

    "Unit": [
        "Days",
        "Days",
        "Percentage",
        "Percentage",
        "Index (Clean = 100)",
        "Ratio (Single / Album)"
    ]
})

# STEP 11: Display KPI results

print("\n====================================")
print("STEP 33: BUSINESS KPI RESULTS")
print("====================================")

print(kpis.to_string(index=False))

print("\nTotal Songs Analysed:", len(song_data))

# STEP 12: Save reports

kpis.to_csv(
    "Spain_Business_KPI_Report.csv",
    index=False
)

song_data.to_csv(
    "Spain_Business_KPI_Details.csv",
    index=False
)

print("\n====================================")
print("STEP 33 COMPLETED SUCCESSFULLY!")
print("KPI report saved!")
print("Detailed report saved!")
print("====================================")
