
import streamlit as st
import pandas as pd

# ==========================================
# SPAIN TOP 50 SONGS - INTERACTIVE DASHBOARD
# ATLANTIC RECORDING CORPORATION
# ==========================================

st.set_page_config(
    page_title="Spain Top 50 Music Dashboard",
    page_icon="🎵",
    layout="wide"
)

# STEP 1: Dashboard heading

st.title("🎵 Spain Top 50 Songs Analysis")
st.subheader("Atlantic Recording Corporation")
st.write("Music Chart Performance and Content Lifecycle Dashboard")

# STEP 2: Load dataset

@st.cache_data
def load_data():
    data = pd.read_csv("Atlantic_Spain_Cleaned.csv")
    data["date"] = pd.to_datetime(data["date"])
    return data

df = load_data()

# STEP 3: Sidebar filters

st.sidebar.header("Dashboard Filters")

artists = sorted(df["artist"].dropna().unique())

selected_artists = st.sidebar.multiselect(
    "Select Artists",
    artists,
    default=artists
)

album_types = sorted(df["album_type"].dropna().unique())

selected_albums = st.sidebar.multiselect(
    "Select Album Type",
    album_types,
    default=album_types
)

filtered = df[
    (df["artist"].isin(selected_artists)) &
    (df["album_type"].isin(selected_albums))
].copy()

# STEP 4: Song-level analysis

song_data = filtered.groupby(
    ["song", "artist"]
).agg(
    chart_days=("date", "nunique"),
    popularity=("popularity", "mean"),
    duration_ms=("duration_ms", "first"),
    first_date=("date", "min"),
    last_date=("date", "max")
).reset_index()

song_data["lifespan_days"] = (
    song_data["last_date"] -
    song_data["first_date"]
).dt.days + 1

song_data["retention_rate"] = (
    song_data["chart_days"] /
    song_data["lifespan_days"]
) * 100

# STEP 5: KPI metrics

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Songs",
    song_data["song"].nunique()
)

col2.metric(
    "Average Chart Days",
    round(song_data["chart_days"].mean(), 2)
    if not song_data.empty else 0
)

col3.metric(
    "Average Popularity",
    round(song_data["popularity"].mean(), 2)
    if not song_data.empty else 0
)

col4.metric(
    "Average Retention",
    f"{song_data['retention_rate'].mean():.2f}%"
    if not song_data.empty else "0%"
)

# STEP 6: Top 10 songs

st.header("🏆 Top 10 Songs by Chart Appearances")

if not song_data.empty:
    top_songs = song_data.nlargest(10, "chart_days")

    st.bar_chart(
        top_songs.set_index("song")["chart_days"],
        horizontal=True
    )

# STEP 7: Popularity analysis

st.header("⭐ Popularity Analysis")

if not song_data.empty:
    popularity_data = song_data.set_index("song")[
        "popularity"
    ]

    st.bar_chart(popularity_data.head(15))

# STEP 8: Album type analysis

st.header("💿 Album Type Distribution")

if not filtered.empty:
    album_distribution = filtered.drop_duplicates(
        subset=["song", "artist"]
    )["album_type"].value_counts()

    st.bar_chart(album_distribution)

# STEP 9: Explicit vs Clean

st.header("🔞 Explicit vs Clean Content")

if not filtered.empty:
    content = filtered.drop_duplicates(
        subset=["song", "artist"]
    ).copy()

    content["Content Type"] = (
        content["is_explicit"]
        .astype(str)
        .str.lower()
        .map({
            "true": "Explicit",
            "false": "Clean",
            "1": "Explicit",
            "0": "Clean"
        })
    )

    st.bar_chart(
        content["Content Type"].value_counts()
    )

# STEP 10: Song duration

st.header("⏱️ Song Duration Analysis")

if not song_data.empty:
    duration = (
        song_data["duration_ms"] / 60000
    )

    duration_distribution = pd.cut(
        duration,
        bins=[0, 2.5, 3.5, 4.5, float("inf")],
        labels=[
            "Short",
            "Medium",
            "Long",
            "Very Long"
        ]
    )

    st.bar_chart(duration_distribution.value_counts())

# STEP 11: Retention analysis

st.header("📈 Song Retention Analysis")

if not song_data.empty:
    retention = song_data.sort_values(
        "retention_rate",
        ascending=False
    )

    st.dataframe(
        retention[
            [
                "song",
                "artist",
                "chart_days",
                "lifespan_days",
                "retention_rate"
            ]
        ],
        use_container_width=True
    )

# STEP 12: Final dataset

st.header("📁 Filtered Dataset")

st.dataframe(
    filtered,
    use_container_width=True
)

st.success("Spain Top 50 Dashboard Loaded Successfully!")
