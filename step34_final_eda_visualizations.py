
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# STEP 34: FINAL EDA VISUALIZATIONS
# SPAIN TOP 50 SONGS
# ==========================================

# STEP 1: Load dataset

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

df["date"] = pd.to_datetime(df["date"])

# Remove duplicate entries

df = df.drop_duplicates(
    subset=["date", "song", "artist"]
)

# STEP 2: Prepare song-level data

song_data = df.groupby(
    ["song", "artist"]
).agg(
    chart_days=("date", "nunique"),
    popularity=("popularity", "mean"),
    duration_ms=("duration_ms", "first"),
    album_type=("album_type", "first"),
    is_explicit=("is_explicit", "first"),
    first_date=("date", "min"),
    last_date=("date", "max")
).reset_index()

# Calculate lifespan and retention

song_data["lifespan_days"] = (
    song_data["last_date"] -
    song_data["first_date"]
).dt.days + 1

song_data["retention_rate"] = (
    song_data["chart_days"] /
    song_data["lifespan_days"]
) * 100

song_data["retention_category"] = pd.cut(
    song_data["retention_rate"],
    bins=[-1, 50, 80, 101],
    labels=["Low", "Medium", "High"]
)

# ==========================================
# CHART 1: TOP 10 SONGS
# ==========================================

top_songs = song_data.nlargest(
    10, "chart_days"
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=top_songs,
    x="chart_days",
    y="song"
)

plt.title("Top 10 Songs by Chart Appearances")
plt.xlabel("Chart Days")
plt.ylabel("Song")

plt.tight_layout()
plt.savefig("Chart_01_Top_10_Songs.png")
plt.close()
# ==========================================
# CHART 2: POPULARITY DISTRIBUTION
# ==========================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=song_data,
    x="popularity",
    bins=20,
    kde=True
)

plt.title("Song Popularity Distribution")
plt.xlabel("Popularity")
plt.ylabel("Number of Songs")

plt.tight_layout()
plt.savefig("Chart_02_Popularity_Distribution.png")
plt.close()

# ==========================================
# CHART 3: ALBUM TYPE DISTRIBUTION
# ==========================================

plt.figure(figsize=(8, 6))

sns.countplot(
    data=song_data,
    x="album_type"
)

plt.title("Album Type Distribution")
plt.xlabel("Album Type")
plt.ylabel("Number of Songs")

plt.tight_layout()
plt.savefig("Chart_03_Album_Type.png")
plt.close()

# ==========================================
# CHART 4: EXPLICIT VS CLEAN
# ==========================================

song_data["content_type"] = (
    song_data["is_explicit"]
    .astype(str)
    .str.lower()
    .map({
        "true": "Explicit",
        "false": "Clean",
        "1": "Explicit",
        "0": "Clean"
    })
)

plt.figure(figsize=(8, 6))

sns.countplot(
    data=song_data,
    x="content_type"
)

plt.title("Explicit vs Clean Songs")
plt.xlabel("Content Type")
plt.ylabel("Number of Songs")

plt.tight_layout()
plt.savefig("Chart_04_Explicit_Clean.png")
plt.close()

# ==========================================
# CHART 5: SONG DURATION
# ==========================================

song_data["duration_minutes"] = (
    song_data["duration_ms"] / 60000
)

plt.figure(figsize=(10, 6))

sns.histplot(
    data=song_data,
    x="duration_minutes",
    bins=20,
    kde=True
)

plt.title("Song Duration Distribution")
plt.xlabel("Duration in Minutes")
plt.ylabel("Number of Songs")

plt.tight_layout()
plt.savefig("Chart_05_Song_Duration.png")
plt.close()

# ==========================================
# CHART 6: RETENTION CATEGORY
# ==========================================

plt.figure(figsize=(8, 6))

sns.countplot(
    data=song_data,
    x="retention_category",
    order=["High", "Medium", "Low"]
)

plt.title("Song Retention Categories")
plt.xlabel("Retention Category")
plt.ylabel("Number of Songs")

plt.tight_layout()
plt.savefig("Chart_06_Retention_Category.png")
plt.close()

# ==========================================
# COMPLETION
# ==========================================

print("\n================================")
print("STEP 34 COMPLETED SUCCESSFULLY!")
print("================================")

print("Total songs analysed:", len(song_data))

print("\nAll six visualization charts saved!")
print("All 6 charts generated successfully!")
