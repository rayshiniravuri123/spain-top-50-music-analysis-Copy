
import pandas as pd

# ==========================================
# STEP 37: BUSINESS INSIGHTS AND RECOMMENDATIONS
# SPAIN TOP 50 SONGS
# ATLANTIC RECORDING CORPORATION
# ==========================================

# STEP 1: Load dataset

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

df["date"] = pd.to_datetime(df["date"])

df = df.drop_duplicates(
    subset=["date", "song", "artist"]
)

# STEP 2: Calculate song performance

song_data = df.groupby(
    ["song", "artist"]
).agg(
    chart_days=("date", "nunique"),
    average_popularity=("popularity", "mean"),
    duration_ms=("duration_ms", "first"),
    first_date=("date", "min"),
    last_date=("date", "max"),
    album_type=("album_type", "first"),
    is_explicit=("is_explicit", "first"),
    best_position=("position", "min")
).reset_index()

# STEP 3: Calculate retention

song_data["lifespan_days"] = (
    song_data["last_date"] -
    song_data["first_date"]
).dt.days + 1

song_data["retention_rate"] = (
    song_data["chart_days"] /
    song_data["lifespan_days"]
) * 100

song_data["duration_minutes"] = (
    song_data["duration_ms"] / 60000
)

# STEP 4: Prepare report

report = []

report.append("SPAIN TOP 50 SONGS")
report.append("BUSINESS INSIGHTS AND RECOMMENDATIONS")
report.append("=" * 55)

# INSIGHT 1: Chart longevity

top_songs = song_data.nlargest(5, "chart_days")

report.append("\n1. TOP SONGS BY CHART LONGEVITY")

for _, row in top_songs.iterrows():
    report.append(
        f"{row['song']} - {row['artist']}: "
        f"{row['chart_days']} chart days"
    )

# INSIGHT 2: Popularity

top_popular = song_data.nlargest(
    5, "average_popularity"
)

report.append("\n2. MOST POPULAR SONGS")

for _, row in top_popular.iterrows():
    report.append(
        f"{row['song']}: "
        f"Average popularity {row['average_popularity']:.2f}"
    )

# INSIGHT 3: Album type

album_analysis = song_data.groupby(
    "album_type"
).agg(
    songs=("song", "nunique"),
    average_chart_days=("chart_days", "mean")
).reset_index()

report.append("\n3. ALBUM TYPE PERFORMANCE")

for _, row in album_analysis.iterrows():
    report.append(
        f"{row['album_type']}: "
        f"{row['songs']} songs, "
        f"average chart days "
        f"{row['average_chart_days']:.2f}"
    )

if not album_analysis.empty:
    best_album = album_analysis.loc[
        album_analysis["average_chart_days"].idxmax()
    ]

    report.append(
        f"Best-performing album type: {best_album['album_type']}"
    )

# INSIGHT 4: Explicit vs Clean

song_data["content_type"] = (
    song_data["is_explicit"]
    .astype(str)
    .str.lower()
    .str.strip()
    .map({
        "true": "Explicit",
        "false": "Clean",
        "1": "Explicit",
        "0": "Clean"
    })
)

content_analysis = song_data.groupby(
    "content_type"
).agg(
    total_songs=("song", "nunique"),
    average_chart_days=("chart_days", "mean")
).reset_index()

report.append("\n4. EXPLICIT VS CLEAN PERFORMANCE")

for _, row in content_analysis.iterrows():
    report.append(
        f"{row['content_type']}: "
        f"{row['total_songs']} songs, "
        f"average chart days "
        f"{row['average_chart_days']:.2f}"
    )

# INSIGHT 5: Song duration

duration_average = song_data[
    "duration_minutes"
].mean()

report.append("\n5. SONG DURATION ANALYSIS")

report.append(
    f"Average song duration: {duration_average:.2f} minutes"
)

# INSIGHT 6: Retention

average_retention = song_data[
    "retention_rate"
].mean()

report.append("\n6. RETENTION PERFORMANCE")

report.append(
    f"Average retention rate: {average_retention:.2f}%"
)

# BUSINESS RECOMMENDATIONS

report.append("\n" + "=" * 55)
report.append("BUSINESS RECOMMENDATIONS")
report.append("=" * 55)

report.append(
    "\n1. Study long-lasting songs to identify "
    "successful playlist characteristics."
)

report.append(
    "\n2. Monitor highly popular songs for "
    "playlist promotion opportunities."
)

report.append(
    "\n3. Compare album types before deciding "
    "release and promotional strategies."
)

report.append(
    "\n4. Evaluate explicit and clean content "
    "performance to support playlist planning."
)

report.append(
    "\n5. Use song duration patterns to understand "
    "the content mix of successful tracks."
)

report.append(
    "\n6. Monitor retention to identify songs "
    "that maintain consistent chart presence."
)

# SAVE REPORT

with open(
    "Spain_Business_Insights_Report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(report))

# DISPLAY REPORT

print("\n".join(report))

print("\n========================================")
print("STEP 37 COMPLETED SUCCESSFULLY!")
print("Business insights report saved!")
print("========================================")
