# How to create the Excel sheet and set parameters

## What you are building

4 sheets (plus a guide):

| Sheet | Purpose |
|-------|---------|
| **1_Parameters** | Fixed settings: lines, weights, targets, bonus £, rules |
| **2_Actuals** | Monthly numbers you type (yellow) |
| **3_Scorecard** | Formulas: Actual → Score % → Weighted |
| **4_Bonus** | Plant average + gatekeepers + payout |

Ready-made file: **`Excel_Create_KPI_Template.xlsx`**  
(Also see `Excel_KPI_Calculator.xlsx` which includes demo numbers.)

---

## Part 1 — Create the workbook

1. Open Excel → **Blank workbook**
2. Rename `Sheet1` → `1_Parameters`
3. Add sheets: `2_Actuals`, `3_Scorecard`, `4_Bonus`
4. Colour rule:
   - **Yellow** = type here (inputs)
   - **Blue** = parameters (weights/targets)
   - **Green** = formulas (do not overwrite)

---

## Part 2 — Parameters to create (`1_Parameters`)

### A) Line parameters

| Parameter | Example | Notes |
|-----------|---------|-------|
| Line code | P1, T1, T2, L8, L9 | Column headers on Actuals |
| Machine name | Pancake / Tortilla wrap / L8 / L9 | For reports |
| Include in bonus? | Yes | Yes/No |

### B) KPI parameters (most important)

| KPI | Weight | Direction | Year 1 Target | Unit |
|-----|--------|-----------|---------------|------|
| OEE | **20%** | Higher better | **82** | % |
| Breakdown Frequency | **10%** | Lower better | **15** | count / line / month |
| Breakdown Hours | **15%** | Lower better | **20** | hours / line / month |
| PM Compliance | **20%** | Higher better | **98** | % |
| MTTR | **15%** | Lower better | **2.5** | hours |
| MTBF | **10%** | Higher better | **150** | hours |
| Safety (LTI) | **10%** | Zero LTI | **0** | LTI count |

Check: `=SUM(weights)` must equal **100%**.

### C) Rule parameters

| Parameter | Value |
|-----------|-------|
| Max individual KPI score | 100% |
| Max overall score | 100% |
| LTI > 0 → multiply bonus by | 50% |
| Red audit → multiply bonus by | 50% |
| Major safety / EPW / dishonest | bonus = 0% |

### D) Bonus opportunity parameters (£)

| Shift | Role | Opportunity |
|-------|------|-------------|
| Day | Maint eng / electrician etc. | 324 |
| Day | Multi-skilled | 486 |
| Day | Team leaders | 810 |
| Night | Team leaders | 1020 |
| … | (full list in template) | … |

---

## Part 3 — Actual parameters (`2_Actuals`)

Create a table:

- **Row headers** = parameter names (below)
- **Columns** = P1 | T1 | T2 | L8 | L9
- Put **Month** in cell B2 (e.g. `2026-07`)

| Row | Parameter to enter | Source |
|-----|-------------------|--------|
| Planned production hours | Production plan |
| Actual operating hours | Excel / line log |
| Ideal rate (units/hour) | Engineering |
| Actual output units | Production |
| Good units | Quality |
| Breakdown count | Teams + Maintainer |
| Breakdown hours | Downtime Excel |
| Planned PM jobs | Maintainer |
| Completed PM on time | Maintainer |
| Operational hours | Excel runtime |
| LTI count | H&S |
| Major safety (0/1) | H&S |
| Major EPW (0/1) | Operations |
| Dishonest reporting (0/1) | Management |
| Audit (green/amber/red) | Audit team |

Add **Data Validation** dropdowns for Audit and 0/1 flags.

---

## Part 4 — Scorecard formulas (`3_Scorecard`)

For each line and each KPI, create 4 columns:

`Actual | Target | Score % | Weighted`

**Link Target and Weight to Parameters** (so one change updates all lines):

```excel
Weight  = 1_Parameters!C13      # example OEE weight
Target  = 1_Parameters!E13      # example OEE Year1 target
```

**Score rules:**

```excel
# Higher better (OEE, PM, MTBF)
=MIN(100, Actual/Target*100)

# Lower better (BF, BH, MTTR)
=IF(Actual=0, 100, MIN(100, Target/Actual*100))

# Safety
=IF(LTI=0, 100, 0)

# Weighted
=Score * Weight

# Line total
=MIN(100, SUM(all Weighted))
```

**OEE Actual:**

```excel
=(OpHrs/PlanHrs) * ((Output/OpHrs)/IdealRate) * (Good/Output) * 100
```

**PM Actual:** `=Completed/Planned*100`  
**MTTR Actual:** `=BreakdownHours/BreakdownCount`  
**MTBF Actual:** `=OperationalHours/BreakdownCount`

---

## Part 5 — Bonus sheet (`4_Bonus`)

```excel
Plant_Score = AVERAGE(P1, T1, T2, L8, L9 scores)

Final_Score =
  IF major safety/EPW/dishonest → 0
  ELSE IF LTI>0 → Plant_Score * 0.5
  ELSE Plant_Score
  then IF red audit → × 0.5

Payout = Opportunity_£ * Final_Score / 100
```

---

## Fastest path

1. Open **`Excel_Create_KPI_Template.xlsx`**
2. Set/confirm values on **`1_Parameters`**
3. Type monthly numbers on **`2_Actuals`** (yellow)
4. Read results on **`3_Scorecard`** and **`4_Bonus`**

You do **not** need to rebuild formulas every month — only Actuals change.
