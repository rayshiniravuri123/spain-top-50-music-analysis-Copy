
import pandas as pd

# STEP 29: EXPLICIT VS CLEAN RETENTION

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

# Convert explicit column into readable categories

df["is_explicit"] = df["is_explicit"].astype(str).str.lower()

df["content_type"] = df["is_explicit"].map({
    "true": "Explicit",
    "false": "Clean"
})

# Calculate retention by song

song_retention = df.groupby(
    ["song", "artist", "content_type"]
).agg(
    chart_days=("date", "nunique"),
    first_date=("date", "min"),
    last_date=("date", "max")
).reset_index()

# Calculate lifespan

song_retention["first_date"] = pd.to_datetime(
    song_retention["first_date"]
)

song_retention["last_date"] = pd.to_datetime(
    song_retention["last_date"]
)

song_retention["lifespan_days"] = (
    song_retention["last_date"]
    - song_retention["first_date"]
).dt.days + 1

# Calculate retention percentage

song_retention["retention_rate"] = (
    song_retention["chart_days"]
    / song_retention["lifespan_days"]
) * 100

# Compare content types

comparison = song_retention.groupby(
    "content_type"
).agg(
    total_songs=("song", "nunique"),
    average_chart_days=("chart_days", "mean"),
    average_lifespan=("lifespan_days", "mean"),
    average_retention=("retention_rate", "mean")
).reset_index()

print("\n===== STEP 29: EXPLICIT VS CLEAN =====")

print(comparison.to_string(index=False))

# Save results

comparison.to_csv(
    "Spain_Explicit_Clean_Retention.csv",
    index=False
)

print("\nAnalysis completed!")
print("Report saved successfully!")
