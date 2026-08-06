# Signature Flatbreads — KPI Tracker

> **New / junior analyst?** Start here first:  
> **[`docs/JUNIOR_ANALYST_GUIDE.md`](docs/JUNIOR_ANALYST_GUIDE.md)**  
> (plain-English explanation with examples)

Data-analyst toolkit for the **Maintenance Team KPI & Monthly Bonus Scheme (V2)**.

## Lines covered

| Code | Machinery |
|------|-----------|
| **P1** | Pancake |
| **T1**, **T2** | Tortilla wrap |
| **L8**, **L9** | Lines L8 / L9 |

## Quick start (Excel — recommended for the plant)

**Create sheet + set parameters:** [`docs/CREATE_EXCEL_AND_PARAMETERS.md`](docs/CREATE_EXCEL_AND_PARAMETERS.md)  
**Blank template (parameters ready):** [`Excel_Create_KPI_Template.xlsx`](Excel_Create_KPI_Template.xlsx)  
**Demo with sample numbers:** [`Excel_KPI_Calculator.xlsx`](Excel_KPI_Calculator.xlsx)

1. Open the template → confirm **`1_Parameters`** (weights, targets, bonus £)
2. Type monthly actuals on **`2_Actuals`** (yellow) for **P1, T1, T2, L8, L9**
3. Read **`3_Scorecard`** and **`4_Bonus`**

Formula guide: [`docs/EXCEL_HOW_TO.md`](docs/EXCEL_HOW_TO.md)

## Optional: Python / notebook

1. Read the scheme: [`docs/KPI_SCHEME.md`](docs/KPI_SCHEME.md)
2. Copy the blank month file and fill actuals from Excel / Maintainer / Teams:
   ```bash
   cp data/monthly_actuals_TEMPLATE.csv data/monthly_actuals_2026-07.csv
   ```
3. Run the calculator:
   ```bash
   python kpi_calculator.py
   ```
4. Open the Excel report in `output/`.

## What you need to collect each month (per line)

| Field | Source (typical) | Used for |
|-------|------------------|----------|
| Planned production hours | Production plan / Excel | OEE availability |
| Actual operating hours | Excel / line log | OEE, MTBF |
| Ideal rate (units/hour) | Standards | OEE performance |
| Actual output units | Production | OEE performance |
| Good units | Quality | OEE quality |
| Breakdown count | Teams / Maintainer | BF, MTTR, MTBF |
| Breakdown hours | Excel downtime | BH, MTTR |
| Planned PM jobs | Maintainer | PM compliance |
| Completed PM on time | Maintainer (job completion date) | PM compliance |
| Operational hours | Excel | MTBF |
| LTI count | Safety | Safety KPI + gate |
| Major safety / EPW / audit | Safety / audits | Bonus gatekeepers |

## Year 1 targets (per line where noted)

| KPI | Weight | Target |
|-----|--------|--------|
| OEE | 20% | 82% |
| Breakdown Frequency | 10% | ≤ 15 / line / month |
| Breakdown Hours | 15% | ≤ 20 hrs / line / month |
| PM Compliance | 20% | ≥ 98% |
| MTTR | 15% | < 2.5 hrs |
| MTBF | 10% | > 150 hrs |
| Safety | 10% | Zero LTI |

## Scoring rules (short)

- Higher-is-better: `(Actual ÷ Target) × 100`, capped at 100%
- Lower-is-better: `(Target ÷ Actual) × 100`, capped at 100%
- Plant bonus score = average of line scores, then apply gatekeepers
- LTI > 0 → overall bonus × 50%; major safety / EPW / dishonest reporting → 0%; red audit → × 50%

## Files

```
signature_flatbread_kpi/
  config/kpi_scheme.json          # weights, targets, bonus opportunities
  data/monthly_actuals_TEMPLATE.csv
  data/monthly_actuals_SAMPLE.csv # demo numbers so you can see the maths
  docs/KPI_SCHEME.md
  kpi_calculator.py
  KPI_Dashboard.ipynb
  output/                         # generated Excel reports
```

Sample data is **demo only** — replace with real plant figures before sharing with your manager.
