# ============================================================
# Clean huge data (~17,000 rows) + plot graphs
# Beginner Python code for Signature Flatbreads / any CSV
# ============================================================
# Install once:
#   pip install pandas matplotlib seaborn
#
# Run:
#   python clean_data_and_plot.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------
# 1) LOAD DATA
# --------------------------
# Change this path to YOUR file
file_path = "data/raw/plant_events_17k_SAMPLE.csv"   # or r"C:\Users\You\Desktop\my_data.csv"

df = pd.read_csv(file_path)
print("Before cleaning:", df.shape)
print(df.head())

# --------------------------
# 2) CLEAN DATA
# --------------------------

# Clean column names
df.columns = (
    df.columns.astype(str)
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
    .str.replace(r"\s+", "_", regex=True)
)

# Remove fully empty rows
df = df.dropna(how="all")

# Trim spaces in text columns
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace({"": np.nan, "nan": np.nan, "None": np.nan})

# Convert date/time columns
for col in df.columns:
    if "date" in col.lower() or "time" in col.lower():
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Fix Line names like " p1 " -> "P1"
if "Line" in df.columns:
    df["Line"] = df["Line"].astype(str).str.strip().str.upper()

# Fix Shift names like "day" / "NIGHT" -> "Day" / "Night"
if "Shift" in df.columns:
    df["Shift"] = df["Shift"].astype(str).str.strip().str.title()

# Convert important columns to numbers
for col in df.columns:
    name = col.lower()
    if any(k in name for k in ["hour", "unit", "count", "downtime", "output", "good", "oee", "rate"]):
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove impossible downtime values
if "Downtime_Hours" in df.columns:
    df.loc[(df["Downtime_Hours"] < 0) | (df["Downtime_Hours"] > 24), "Downtime_Hours"] = np.nan

# Good units cannot be more than output
if "Good_Units" in df.columns and "Output_Units" in df.columns:
    bad = df["Good_Units"] > df["Output_Units"]
    df.loc[bad, "Good_Units"] = df.loc[bad, "Output_Units"]

# Fill missing numbers with median
for col in df.select_dtypes(include="number").columns:
    if df[col].isna().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

# Fill missing text with Unknown
for col in df.select_dtypes(include=["object", "string"]).columns:
    if df[col].isna().sum() > 0:
        df[col] = df[col].fillna("Unknown")

# Remove duplicate rows
df = df.drop_duplicates()

# Cap extreme downtime outliers
if "Downtime_Hours" in df.columns:
    q1 = df["Downtime_Hours"].quantile(0.25)
    q3 = df["Downtime_Hours"].quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 3 * iqr
    df["Downtime_Hours"] = df["Downtime_Hours"].clip(upper=upper)

df = df.reset_index(drop=True)
print("After cleaning:", df.shape)

# Save cleaned file
Path("data/cleaned").mkdir(parents=True, exist_ok=True)
cleaned_path = "data/cleaned/cleaned_data.csv"
df.to_csv(cleaned_path, index=False)
print("Saved cleaned file:", cleaned_path)

# --------------------------
# 3) PLOT GRAPHS
# --------------------------
Path("plots").mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid")

# Graph 1: Records by Line
if "Line" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Line", order=df["Line"].value_counts().index, color="#1F4E79")
    plt.title("Records by Line")
    plt.xlabel("Line")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("plots/01_records_by_line.png", dpi=140)
    plt.show()

# Graph 2: Total Downtime by Line
if "Line" in df.columns and "Downtime_Hours" in df.columns:
    g = df.groupby("Line", as_index=False)["Downtime_Hours"].sum()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=g, x="Line", y="Downtime_Hours", color="#C0392B")
    plt.title("Total Downtime Hours by Line")
    plt.tight_layout()
    plt.savefig("plots/02_downtime_by_line.png", dpi=140)
    plt.show()

# Graph 3: Event type pie chart
if "Event_Type" in df.columns:
    vc = df["Event_Type"].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(vc.values, labels=vc.index, autopct="%1.0f%%", startangle=90)
    plt.title("Event Type Mix")
    plt.tight_layout()
    plt.savefig("plots/03_event_type_mix.png", dpi=140)
    plt.show()

# Graph 4: Daily downtime trend
time_col = None
for c in df.columns:
    if "time" in c.lower() or "date" in c.lower():
        time_col = c
        break

if time_col and "Downtime_Hours" in df.columns:
    daily = (
        df.dropna(subset=[time_col])
        .assign(Day=df[time_col].dt.floor("D"))
        .groupby("Day", as_index=False)["Downtime_Hours"]
        .sum()
    )
    plt.figure(figsize=(10, 5))
    plt.plot(daily["Day"], daily["Downtime_Hours"], color="#1F4E79")
    plt.title("Daily Total Downtime Hours")
    plt.xlabel("Day")
    plt.ylabel("Downtime Hours")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("plots/04_daily_downtime_trend.png", dpi=140)
    plt.show()

# Graph 5: Output vs Good Units
if "Output_Units" in df.columns and "Good_Units" in df.columns:
    sample = df.sample(min(3000, len(df)), random_state=42)
    plt.figure(figsize=(7, 6))
    plt.scatter(sample["Output_Units"], sample["Good_Units"], alpha=0.25, s=12, c="#1F4E79")
    lim = max(sample["Output_Units"].max(), sample["Good_Units"].max())
    plt.plot([0, lim], [0, lim], "r--", label="Good = Output")
    plt.title("Output vs Good Units")
    plt.xlabel("Output Units")
    plt.ylabel("Good Units")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plots/05_output_vs_good.png", dpi=140)
    plt.show()

print("All graphs saved in plots/ folder")
