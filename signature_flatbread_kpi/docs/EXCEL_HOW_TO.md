# How to calculate KPIs in Excel (Signature Flatbreads)

## Colour coding in `Excel_KPI_Calculator.xlsx`

| Colour | Meaning |
|--------|---------|
| Yellow | Type your **Actual** numbers |
| Blue | **Target** (Year 1 scheme) |
| Green | **Formula** — auto-calculated |

---

## Step-by-step

1. Open **`Excel_KPI_Calculator.xlsx`**
2. Go to **`1_Actuals_Input`** — enter data for **P1, T1, T2, L8, L9** (yellow cells)
3. Go to **`2_KPI_Scorecard`** — Actual, Score %, and Weighted points calculate automatically
4. Go to **`3_Plant_Bonus`** — plant average score, gatekeepers, and bonus payout by role

---

## The two scoring rules

**Higher is better** (OEE, PM Compliance, MTBF):

```excel
=MIN(100, Actual/Target*100)
```

**Lower is better** (Breakdown Frequency, Breakdown Hours, MTTR):

```excel
=IF(Actual=0, 100, MIN(100, Target/Actual*100))
```

`MIN(100, …)` caps every score at **100%** (scheme rule).

---

## Formulas per KPI (Year 1)

Assume one line’s inputs are in column **C** on your Actuals sheet:

| Cell | What you type |
|------|----------------|
| C6 | Planned production hours |
| C7 | Actual operating hours |
| C8 | Ideal rate (units/hour) |
| C9 | Actual output units |
| C10 | Good units |
| C11 | Breakdown count |
| C12 | Breakdown hours |
| C13 | Planned PM jobs |
| C14 | Completed PM on time |
| C15 | Operational hours |
| C16 | LTI count |

### 1) OEE (weight 20%, target 82%)

```excel
= (C7/C6) * ((C9/C7)/C8) * (C10/C9) * 100
```

```excel
Score   = MIN(100, OEE_Actual/82*100)
Weighted = Score * 0.20
```

**Example:** Actual 78% → `78/82*100 = 95.1%` → weighted `95.1 × 20% = 19.0`

### 2) Breakdown Frequency (weight 10%, target ≤ 15)

```excel
Actual = C11
Score  = IF(C11=0, 100, MIN(100, 15/C11*100))
Weighted = Score * 0.10
```

### 3) Breakdown Hours (weight 15%, target ≤ 20)

```excel
Actual = C12
Score  = IF(C12=0, 100, MIN(100, 20/C12*100))
Weighted = Score * 0.15
```

**Example:** Actual 18 → `20/18*100 = 111%` → capped to **100%** → weighted `15.0`

### 4) PM Compliance (weight 20%, target ≥ 98%)

```excel
Actual = C14/C13*100
Score  = MIN(100, Actual/98*100)
Weighted = Score * 0.20
```

**Example:** Actual 96% → `96/98*100 = 98.0%` → weighted `19.6`

### 5) MTTR (weight 15%, target < 2.5 hrs)

```excel
Actual = IF(C11=0, 0, C12/C11)
Score  = IF(Actual=0, 100, MIN(100, 2.5/Actual*100))
Weighted = Score * 0.15
```

**Example:** Actual 3.0 hrs → `2.5/3.0*100 = 83.3%` → weighted `12.5`

### 6) MTBF (weight 10%, target > 150 hrs)

```excel
Actual = IF(C11=0, C15, C15/C11)
Score  = MIN(100, Actual/150*100)
Weighted = Score * 0.10
```

**Example:** Actual 160 → `160/150*100 = 106.7%` → capped to **100%** → weighted `10.0`

### 7) Safety (weight 10%, target Zero LTI)

```excel
Score    = IF(C16=0, 100, 0)
Weighted = Score * 0.10
```

---

## Final line score

```excel
=MIN(100, OEE_W + BF_W + BH_W + PM_W + MTTR_W + MTBF_W + Safety_W)
```

**Printed example total:** `19.0 + 10.0 + 15.0 + 19.6 + 12.5 + 10.0 + 10.0 = 96.1%`

## Plant bonus score

```excel
=AVERAGE(P1_score, T1_score, T2_score, L8_score, L9_score)
```

Then apply gatekeepers:

| Condition | Effect |
|-----------|--------|
| LTI > 0 | × 50% |
| Major safety / EPW / dishonest reporting | = 0% |
| Red audit | × 50% |

## Bonus payout

```excel
= Monthly_Opportunity * Final_Bonus_Score / 100
```

**Example:** Maintenance eng opportunity 324 × 96.1% = **£311.36**

---

## File location

`signature_flatbread_kpi/Excel_KPI_Calculator.xlsx`
