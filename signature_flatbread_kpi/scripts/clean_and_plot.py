"""
Clean a large CSV (~17k+ rows) and save a cleaned file.

Usage:
  python scripts/clean_and_plot.py
  python scripts/clean_and_plot.py --input data/raw/your_file.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "cleaned"
PLOT_DIR = ROOT / "plots"


def find_default_input() -> Path:
    preferred = RAW_DIR / "plant_events_17k_SAMPLE.csv"
    if preferred.exists():
        return preferred
    csvs = sorted(RAW_DIR.glob("*.csv"), key=lambda p: p.stat().st_size, reverse=True)
    if not csvs:
        raise FileNotFoundError(
            f"No CSV found in {RAW_DIR}. Put your 17,000-row file there and run again."
        )
    return csvs[0]


def load_data(path: Path) -> pd.DataFrame:
    # Try common separators / encodings for messy factory exports
    for kwargs in (
        {"encoding": "utf-8"},
        {"encoding": "utf-8-sig"},
        {"encoding": "latin-1"},
        {"sep": ";", "encoding": "utf-8-sig"},
    ):
        try:
            df = pd.read_csv(path, low_memory=False, **kwargs)
            if df.shape[1] >= 2:
                print(f"Loaded {path.name}: {len(df):,} rows × {df.shape[1]} columns")
                return df
        except Exception:
            continue
    raise ValueError(f"Could not read {path}")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df


def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Generic + plant-aware cleaning. Returns cleaned df and a report dict."""
    report: dict = {"start_rows": len(df), "steps": []}
    df = standardize_columns(df)

    # Drop fully empty rows/columns
    before = len(df)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    report["steps"].append(f"Dropped fully empty rows/cols ({before - len(df)} rows removed)")

    # Trim text columns
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"": np.nan, "nan": np.nan, "None": np.nan, "NaT": np.nan})

    # Parse dates if present
    for col in df.columns:
        if any(k in col.lower() for k in ("date", "time", "timestamp")):
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=False)

    # Line cleanup (P1 / T1 style)
    if "Line" in df.columns:
        df["Line"] = df["Line"].astype(str).str.strip().str.upper()
        df["Line"] = df["Line"].replace({"NAN": np.nan})

    # Shift cleanup
    if "Shift" in df.columns:
        df["Shift"] = (
            df["Shift"]
            .astype(str)
            .str.strip()
            .str.title()
            .replace({"Nan": np.nan})
        )

    # Numeric columns
    for col in df.columns:
        if any(k in col.lower() for k in ("hour", "unit", "count", "oee", "pct", "rate", "downtime", "output", "good", "lti", "mttr", "mtbf")):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Business rules if columns exist
    if "Downtime_Hours" in df.columns:
        invalid = (df["Downtime_Hours"] < 0) | (df["Downtime_Hours"] > 24)
        n_inv = int(invalid.fillna(False).sum())
        df.loc[invalid, "Downtime_Hours"] = np.nan
        report["steps"].append(f"Set {n_inv} invalid Downtime_Hours (<0 or >24) to missing")

    if {"Good_Units", "Output_Units"}.issubset(df.columns):
        bad_q = df["Good_Units"] > df["Output_Units"]
        n_bad = int(bad_q.fillna(False).sum())
        df.loc[bad_q, "Good_Units"] = df.loc[bad_q, "Output_Units"]
        report["steps"].append(f"Fixed {n_bad} rows where Good_Units > Output_Units")

    # Fill numeric missings with median (simple junior-friendly approach)
    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        miss = int(df[col].isna().sum())
        if miss:
            med = df[col].median()
            df[col] = df[col].fillna(med)
            report["steps"].append(f"Filled {miss} missing {col} with median={med}")

    # Fill categorical missings
    for col in df.select_dtypes(include=["object", "string"]).columns:
        miss = int(df[col].isna().sum())
        if miss:
            df[col] = df[col].fillna("Unknown")
            report["steps"].append(f"Filled {miss} missing {col} with 'Unknown'")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    report["steps"].append(f"Removed {before - len(df)} duplicate rows")

    # Optional IQR outlier winsorize for downtime
    if "Downtime_Hours" in df.columns:
        q1, q3 = df["Downtime_Hours"].quantile([0.25, 0.75])
        iqr = q3 - q1
        hi = q3 + 3 * iqr
        n_out = int((df["Downtime_Hours"] > hi).sum())
        df["Downtime_Hours"] = df["Downtime_Hours"].clip(upper=hi)
        report["steps"].append(f"Capped {n_out} Downtime_Hours outliers above {hi:.2f}")

    df = df.reset_index(drop=True)
    report["end_rows"] = len(df)
    report["columns"] = list(df.columns)
    return df, report


def make_plots(df: pd.DataFrame, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")
    paths: list[Path] = []

    # 1) Rows by Line
    if "Line" in df.columns:
        fig, ax = plt.subplots(figsize=(9, 5))
        order = df["Line"].value_counts().index
        sns.countplot(data=df, x="Line", order=order, ax=ax, color="#1F4E79")
        ax.set_title("Records by Line")
        ax.set_xlabel("Line")
        ax.set_ylabel("Count")
        p = out_dir / "01_records_by_line.png"
        fig.tight_layout()
        fig.savefig(p, dpi=140)
        plt.close(fig)
        paths.append(p)

    # 2) Downtime by Line
    if {"Line", "Downtime_Hours"}.issubset(df.columns):
        fig, ax = plt.subplots(figsize=(9, 5))
        g = df.groupby("Line", as_index=False)["Downtime_Hours"].sum()
        sns.barplot(data=g, x="Line", y="Downtime_Hours", ax=ax, color="#C0392B")
        ax.set_title("Total Downtime Hours by Line")
        p = out_dir / "02_downtime_by_line.png"
        fig.tight_layout()
        fig.savefig(p, dpi=140)
        plt.close(fig)
        paths.append(p)

    # 3) Event type mix
    if "Event_Type" in df.columns:
        fig, ax = plt.subplots(figsize=(9, 5))
        vc = df["Event_Type"].value_counts()
        ax.pie(vc.values, labels=vc.index, autopct="%1.0f%%", startangle=90)
        ax.set_title("Event Type Mix")
        p = out_dir / "03_event_type_mix.png"
        fig.tight_layout()
        fig.savefig(p, dpi=140)
        plt.close(fig)
        paths.append(p)

    # 4) Daily downtime trend
    time_col = next((c for c in df.columns if "time" in c.lower() or "date" in c.lower()), None)
    if time_col and "Downtime_Hours" in df.columns and pd.api.types.is_datetime64_any_dtype(df[time_col]):
        daily = (
            df.dropna(subset=[time_col])
            .assign(Day=lambda x: x[time_col].dt.floor("D"))
            .groupby("Day", as_index=False)["Downtime_Hours"]
            .sum()
        )
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.plot(daily["Day"], daily["Downtime_Hours"], color="#1F4E79", linewidth=1.5)
        ax.set_title("Daily Total Downtime Hours")
        ax.set_xlabel("Day")
        ax.set_ylabel("Downtime Hours")
        fig.autofmt_xdate()
        p = out_dir / "04_daily_downtime_trend.png"
        fig.tight_layout()
        fig.savefig(p, dpi=140)
        plt.close(fig)
        paths.append(p)

    # 5) Output vs Good scatter (sample if huge)
    if {"Output_Units", "Good_Units"}.issubset(df.columns):
        sample = df.sample(min(3000, len(df)), random_state=42)
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.scatter(sample["Output_Units"], sample["Good_Units"], alpha=0.25, s=12, c="#1F4E79")
        lim = max(sample["Output_Units"].max(), sample["Good_Units"].max())
        ax.plot([0, lim], [0, lim], "r--", label="Good = Output")
        ax.set_title("Output vs Good Units (sample)")
        ax.set_xlabel("Output Units")
        ax.set_ylabel("Good Units")
        ax.legend()
        p = out_dir / "05_output_vs_good.png"
        fig.tight_layout()
        fig.savefig(p, dpi=140)
        plt.close(fig)
        paths.append(p)

    # 6) Generic fallback: histogram of first numeric column
    if not paths:
        num = df.select_dtypes(include="number")
        if not num.empty:
            col = num.columns[0]
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.histplot(df[col].dropna(), bins=40, ax=ax, color="#1F4E79")
            ax.set_title(f"Distribution of {col}")
            p = out_dir / f"01_hist_{col}.png"
            fig.tight_layout()
            fig.savefig(p, dpi=140)
            plt.close(fig)
            paths.append(p)

    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean large CSV and plot graphs")
    parser.add_argument("--input", type=Path, default=None, help="Path to raw CSV")
    args = parser.parse_args()

    raw_path = args.input or find_default_input()
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    df_raw = load_data(raw_path)
    df_clean, report = clean_dataframe(df_raw)

    out_csv = CLEAN_DIR / f"{raw_path.stem}_CLEANED.csv"
    df_clean.to_csv(out_csv, index=False)

    report_path = CLEAN_DIR / f"{raw_path.stem}_CLEANING_REPORT.txt"
    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"Input: {raw_path}\n")
        f.write(f"Start rows: {report['start_rows']:,}\n")
        f.write(f"End rows: {report['end_rows']:,}\n")
        f.write(f"Columns: {report['columns']}\n\n")
        f.write("Steps:\n")
        for s in report["steps"]:
            f.write(f"- {s}\n")

    plots = make_plots(df_clean, PLOT_DIR)

    print("\n=== CLEANING SUMMARY ===")
    print(f"Start rows: {report['start_rows']:,}")
    print(f"End rows:   {report['end_rows']:,}")
    for s in report["steps"]:
        print(" -", s)
    print(f"\nCleaned CSV: {out_csv}")
    print(f"Report:      {report_path}")
    print("Plots:")
    for p in plots:
        print(" -", p)


if __name__ == "__main__":
    main()
