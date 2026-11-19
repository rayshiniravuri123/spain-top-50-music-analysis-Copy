
import pandas as pd

# ==========================================
# STEP 28: RETENTION STABILITY ANALYSIS
# SPAIN TOP 50 SONGS
# ==========================================

# STEP 1: Load dataset

df = pd.read_csv("Atlantic_Spain_Cleaned.csv")

df["date"] = pd.to_datetime(df["date"])

# STEP 2: Remove duplicate song entries
# within the same chart date

df = df.sort_values("position")

df = df.drop_duplicates(
    subset=["date", "song", "artist"]
)

# STEP 3: Calculate song retention

retention = df.groupby(
    ["song", "artist"]
).agg(
    total_chart_days=("date", "nunique"),
    first_appearance=("date", "min"),
    last_appearance=("date", "max")
).reset_index()

# STEP 4: Calculate chart lifespan

retention["lifespan_days"] = (
    retention["last_appearance"]
    - retention["first_appearance"]
).dt.days + 1

# STEP 5: Calculate retention rate

retention["retention_rate"] = (
    retention["total_chart_days"]
    / retention["lifespan_days"]
) * 100

# STEP 6: Classify retention stability

def classify_retention(rate):

    if rate >= 80:
        return "High Retention"

    elif rate >= 50:
        return "Medium Retention"

    else:
        return "Low Retention"


retention["retention_category"] = (
    retention["retention_rate"]
    .apply(classify_retention)
)

# STEP 7: Sort results

retention = retention.sort_values(
    by="retention_rate",
    ascending=False
)

# STEP 8: Display results

print("\n===== STEP 28: RETENTION STABILITY =====")

print(retention.head(20).to_string(index=False))

# STEP 9: Save report

retention.to_csv(
    "Spain_Retention_Stability_Analysis.csv",
    index=False
)

print("\nRetention analysis completed!")

print("Total songs analysed:", len(retention))

print("\nRetention categories:")
print(retention["retention_category"].value_counts())

print("\nReport saved successfully!")
