"""Signature Flatbreads — Maintenance KPI calculator.

Implements the V2 Maintenance Team KPI & Monthly Bonus Scheme:
- Per-line KPI scores vs Year 1 targets
- Weighted overall score (capped at 100%)
- Safety / EPW / audit gatekeepers
- Bonus payout from role opportunity × final score
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config" / "kpi_scheme.json"


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _cap(score: float, cap: float = 100.0) -> float:
    if score != score:  # NaN
        return 0.0
    return min(score, cap)


def score_higher_better(actual: float, target: float, cap: float = 100.0) -> float:
    if target <= 0:
        return 0.0
    return _cap((actual / target) * 100.0, cap)


def score_lower_better(actual: float, target: float, cap: float = 100.0) -> float:
    if actual is None or actual != actual:
        return 0.0
    if actual <= 0:
        return cap
    return _cap((target / actual) * 100.0, cap)


def calc_oee(row: pd.Series) -> float:
    planned = float(row["planned_production_hours"])
    actual_op = float(row["actual_operating_hours"])
    ideal_rate = float(row["ideal_rate_units_per_hour"])
    actual_output = float(row["actual_output_units"])
    good = float(row["good_units"])
    total = float(row["actual_output_units"])

    if planned <= 0 or ideal_rate <= 0 or total <= 0:
        return 0.0

    availability = actual_op / planned
    performance = (actual_output / actual_op) / ideal_rate if actual_op > 0 else 0.0
    quality = good / total
    return max(0.0, availability * performance * quality * 100.0)


def calc_pm_compliance(row: pd.Series) -> float:
    planned = float(row["planned_pm_jobs"])
    done = float(row["completed_pm_on_time"])
    if planned <= 0:
        return 0.0
    return (done / planned) * 100.0


def calc_mttr(row: pd.Series) -> float | None:
    count = float(row["breakdown_count"])
    hours = float(row["breakdown_hours"])
    if count <= 0:
        return 0.0  # no breakdowns → excellent MTTR for scoring
    return hours / count


def calc_mtbf(row: pd.Series) -> float | None:
    failures = float(row["breakdown_count"])
    op_hours = float(row["operational_hours"])
    if failures <= 0:
        return op_hours if op_hours > 0 else None
    return op_hours / failures


def score_row(row: pd.Series, config: dict[str, Any], year_key: str = "year1") -> dict[str, Any]:
    kpi_map = {k["id"]: k for k in config["kpis"]}
    cap = float(config["rules"]["cap_individual_score_pct"])

    oee_actual = calc_oee(row)
    bf_actual = float(row["breakdown_count"])
    bh_actual = float(row["breakdown_hours"])
    pm_actual = calc_pm_compliance(row)
    mttr_actual = calc_mttr(row)
    mtbf_actual = calc_mtbf(row)
    lti = int(row.get("lti_count", 0) or 0)

    targets = {kid: kpi_map[kid]["targets"][year_key] for kid in kpi_map}

    scores = {
        "oee": score_higher_better(oee_actual, targets["oee"], cap),
        "breakdown_frequency": score_lower_better(bf_actual, targets["breakdown_frequency"], cap),
        "breakdown_hours": score_lower_better(bh_actual, targets["breakdown_hours"], cap),
        "pm_compliance": score_higher_better(pm_actual, targets["pm_compliance"], cap),
        "mttr": score_lower_better(mttr_actual if mttr_actual is not None else 0, targets["mttr"], cap),
        "mtbf": (
            cap
            if mtbf_actual is None
            else score_higher_better(mtbf_actual, targets["mtbf"], cap)
        ),
        "safety": 100.0 if lti == 0 else 0.0,
    }

    weights = {kid: kpi_map[kid]["weight"] for kid in scores}
    weighted = {kid: round(scores[kid] * weights[kid], 2) for kid in scores}
    raw_total = sum(weighted.values())
    overall = min(raw_total, float(config["rules"]["cap_overall_score_pct"]))

    return {
        "month": row["month"],
        "line": row["line"],
        "line_name": row["line_name"],
        "oee_actual_pct": round(oee_actual, 2),
        "oee_target_pct": targets["oee"],
        "oee_score_pct": round(scores["oee"], 2),
        "oee_weighted": weighted["oee"],
        "breakdown_frequency_actual": bf_actual,
        "breakdown_frequency_target": targets["breakdown_frequency"],
        "breakdown_frequency_score_pct": round(scores["breakdown_frequency"], 2),
        "breakdown_frequency_weighted": weighted["breakdown_frequency"],
        "breakdown_hours_actual": bh_actual,
        "breakdown_hours_target": targets["breakdown_hours"],
        "breakdown_hours_score_pct": round(scores["breakdown_hours"], 2),
        "breakdown_hours_weighted": weighted["breakdown_hours"],
        "pm_compliance_actual_pct": round(pm_actual, 2),
        "pm_compliance_target_pct": targets["pm_compliance"],
        "pm_compliance_score_pct": round(scores["pm_compliance"], 2),
        "pm_compliance_weighted": weighted["pm_compliance"],
        "mttr_actual_hrs": round(mttr_actual, 3) if mttr_actual is not None else None,
        "mttr_target_hrs": targets["mttr"],
        "mttr_score_pct": round(scores["mttr"], 2),
        "mttr_weighted": weighted["mttr"],
        "mtbf_actual_hrs": round(mtbf_actual, 2) if mtbf_actual is not None else None,
        "mtbf_target_hrs": targets["mtbf"],
        "mtbf_score_pct": round(scores["mtbf"], 2),
        "mtbf_weighted": weighted["mtbf"],
        "safety_lti_actual": lti,
        "safety_target": targets["safety"],
        "safety_score_pct": round(scores["safety"], 2),
        "safety_weighted": weighted["safety"],
        "raw_weighted_total": round(raw_total, 2),
        "line_kpi_score_pct": round(overall, 2),
        "major_safety_violation": int(row.get("major_safety_violation", 0) or 0),
        "major_epw": int(row.get("major_epw", 0) or 0),
        "dishonest_reporting": int(row.get("dishonest_reporting", 0) or 0),
        "audit_result": str(row.get("audit_result", "") or "").strip().lower(),
    }


def apply_gatekeepers(plant_score: float, frame: pd.DataFrame, config: dict[str, Any]) -> dict[str, Any]:
    rules = config["rules"]
    notes: list[str] = []
    final = plant_score

    if int(frame["major_safety_violation"].sum()) > 0:
        final = float(rules["major_safety_violation_bonus_pct"])
        notes.append("Major safety violation — bonus set to 0%")
    if int(frame["major_epw"].sum()) > 0:
        final = float(rules["major_epw_bonus_pct"])
        notes.append("Major EPW — bonus set to 0%")
    if int(frame["dishonest_reporting"].sum()) > 0:
        final = float(rules["dishonest_reporting_bonus_pct"])
        notes.append("Dishonest reporting — bonus set to 0%")

    if int(frame["safety_lti_actual"].sum()) > 0 and final > 0:
        final = final * (float(rules["lti_reduces_overall_bonus_to_pct"]) / 100.0)
        notes.append("LTI > 0 — overall bonus reduced to 50%")

    audits = set(frame["audit_result"].dropna().astype(str).str.lower())
    if "red" in audits and final > 0:
        final = final * (float(rules["red_audit_bonus_pct"]) / 100.0)
        notes.append("Red audit — bonus reduced to 50%")
    if "green" in audits and rules.get("green_audit_extra_reward"):
        notes.append("Green audit present — eligible for reward on top of usual bonus (confirm amount with manager)")

    return {
        "plant_kpi_score_before_gates_pct": round(plant_score, 2),
        "final_bonus_score_pct": round(min(final, float(rules["cap_overall_score_pct"])), 2),
        "gatekeeper_notes": "; ".join(notes) if notes else "None",
    }


def calculate_monthly_kpis(
    actuals_csv: Path | str,
    config: dict[str, Any] | None = None,
    year_key: str = "year1",
) -> tuple[pd.DataFrame, dict[str, Any]]:
    config = config or load_config()
    df = pd.read_csv(actuals_csv)
    required = [
        "month",
        "line",
        "line_name",
        "planned_production_hours",
        "actual_operating_hours",
        "ideal_rate_units_per_hour",
        "actual_output_units",
        "good_units",
        "breakdown_count",
        "breakdown_hours",
        "planned_pm_jobs",
        "completed_pm_on_time",
        "operational_hours",
        "lti_count",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in actuals file: {missing}")

    # Drop empty template rows
    df = df.dropna(subset=["breakdown_count"], how="any")
    if df.empty:
        raise ValueError("No actual data rows found. Fill monthly_actuals_TEMPLATE.csv first.")

    scored = pd.DataFrame([score_row(row, config, year_key) for _, row in df.iterrows()])
    plant_score = float(scored["line_kpi_score_pct"].mean())
    gates = apply_gatekeepers(plant_score, scored, config)
    return scored, gates


def bonus_payouts(final_score_pct: float, config: dict[str, Any] | None = None) -> pd.DataFrame:
    config = config or load_config()
    rows = []
    for shift, roles in config["bonus_opportunities"].items():
        for role, opportunity in roles.items():
            payout = round(opportunity * (final_score_pct / 100.0), 2)
            rows.append(
                {
                    "shift": shift,
                    "role": role,
                    "monthly_bonus_opportunity": opportunity,
                    "final_kpi_score_pct": final_score_pct,
                    "bonus_payout": payout,
                }
            )
    return pd.DataFrame(rows)


def targets_table(config: dict[str, Any] | None = None) -> pd.DataFrame:
    config = config or load_config()
    rows = []
    for kpi in config["kpis"]:
        rows.append(
            {
                "kpi": kpi["name"],
                "weight_pct": kpi["weight"] * 100,
                "direction": kpi["direction"],
                "unit": kpi["unit"],
                "year1_target": kpi["targets"]["year1"],
                "year2_target": kpi["targets"]["year2"],
                "year3_target": kpi["targets"]["year3"],
                "world_class_target": kpi["targets"]["world_class"],
            }
        )
    return pd.DataFrame(rows)


def export_excel(
    scored: pd.DataFrame,
    gates: dict[str, Any],
    payouts: pd.DataFrame,
    out_path: Path | str,
    config: dict[str, Any] | None = None,
) -> Path:
    config = config or load_config()
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    summary = pd.DataFrame(
        [
            {
                "metric": "Plant KPI score (avg of lines, before gates)",
                "value": gates["plant_kpi_score_before_gates_pct"],
            },
            {
                "metric": "Final bonus score %",
                "value": gates["final_bonus_score_pct"],
            },
            {
                "metric": "Gatekeeper notes",
                "value": gates["gatekeeper_notes"],
            },
        ]
    )

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        targets_table(config).to_excel(writer, sheet_name="Targets", index=False)
        scored.to_excel(writer, sheet_name="Line KPI Scores", index=False)
        summary.to_excel(writer, sheet_name="Plant Summary", index=False)
        payouts.to_excel(writer, sheet_name="Bonus Payouts", index=False)
        pd.DataFrame(config["lines"]).to_excel(writer, sheet_name="Lines", index=False)

    return out_path


if __name__ == "__main__":
    sample = ROOT / "data" / "monthly_actuals_SAMPLE.csv"
    out = ROOT / "output" / "KPI_Report_SAMPLE.xlsx"
    scored_df, gate_info = calculate_monthly_kpis(sample)
    pay = bonus_payouts(gate_info["final_bonus_score_pct"])
    path = export_excel(scored_df, gate_info, pay, out)
    print("Plant score (before gates):", gate_info["plant_kpi_score_before_gates_pct"])
    print("Final bonus score %:", gate_info["final_bonus_score_pct"])
    print("Notes:", gate_info["gatekeeper_notes"])
    print("Wrote:", path)
    print(scored_df[["line", "line_kpi_score_pct", "oee_actual_pct", "pm_compliance_actual_pct", "mttr_actual_hrs", "mtbf_actual_hrs"]])
