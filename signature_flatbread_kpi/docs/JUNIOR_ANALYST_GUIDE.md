# Junior Data Analyst Guide
# Signature Flatbreads — Maintenance KPI & Bonus (very detailed)

This guide assumes you are new. Read it slowly, in order.  
You do **not** need Python. You only need **Excel**.

---

## 1. What is your job here?

Your manager wants you to measure how well the maintenance team performed this month.

You will:

1. Collect numbers for each machine line  
2. Compare those numbers to a **target** (the goal)  
3. Turn that into a **KPI score %**  
4. That score decides how much **bonus money** the team gets  

Think of it like a school report card:

- Target = pass mark  
- Actual = what the student scored  
- KPI score = how close they got to the pass mark  
- Bonus = reward based on the report card  

---

## 2. What is a KPI?

**KPI** = Key Performance Indicator = an important number we track every month.

Example:

- Target OEE = 82%  
- Actual OEE = 78%  
- So the team almost hit the goal, but not fully  

We have **7 KPIs**. Together they make 100% of the score.

---

## 3. Which machines / lines do you track?

| Code | Meaning | Simple words |
|------|---------|--------------|
| **P1** | Pancake machine | Pancake line |
| **T1** | Tortilla wrap machine 1 | Tortilla line 1 |
| **T2** | Tortilla wrap machine 2 | Tortilla line 2 |
| **L8** | Line L8 | Production line 8 |
| **L9** | Line L9 | Production line 9 |

You must collect data for **each** of these 5 lines, every month.

---

## 4. The 7 KPIs in simple English

### KPI 1 — OEE (weight 20%)
**Meaning:** How effectively the machine ran (availability × speed × quality).

- Target Year 1: **82%**  
- Higher is better  

### KPI 2 — Breakdown Frequency (weight 10%)
**Meaning:** How many times the machine broke down this month.

- Target Year 1: **15 or fewer** breakdowns per line  
- Lower is better  

### KPI 3 — Breakdown Hours (weight 15%)
**Meaning:** Total hours the machine was stopped because of breakdowns.

- Target Year 1: **20 hours or fewer** per line  
- Lower is better  

### KPI 4 — PM Compliance (weight 20%)
**Meaning:** Did we finish planned maintenance jobs on time?

- Formula: completed on time ÷ planned jobs  
- Target Year 1: **98% or more**  
- Higher is better  

### KPI 5 — MTTR (weight 15%)
**Meaning:** Mean Time To Repair = average time to fix a breakdown.

- Formula: breakdown hours ÷ number of breakdowns  
- Target Year 1: **under 2.5 hours**  
- Lower is better (faster repair)  

### KPI 6 — MTBF (weight 10%)
**Meaning:** Mean Time Between Failures = how long the machine runs before it fails again.

- Formula: operating hours ÷ number of breakdowns  
- Target Year 1: **more than 150 hours**  
- Higher is better  

### KPI 7 — Safety (weight 10%)
**Meaning:** Did anyone have a Lost Time Injury (LTI)?

- Target: **0 LTI**  
- If LTI = 0 → Safety score = 100%  
- If LTI = 1 or more → Safety score = 0%, and total bonus is cut in half  

---

## 5. Two types of numbers: Target vs Actual

| Word | Meaning | Who decides it? | Do you change it every month? |
|------|---------|-----------------|-------------------------------|
| **Target** | The goal | Already set in the company scheme | No (usually fixed for Year 1) |
| **Actual** | What really happened | You collect from Excel / Maintainer / Teams | **Yes — every month** |

Example for Breakdown Hours on P1:

- Target = 20 hours  
- Actual this month = 18 hours  
- Good news: actual is better than target  

---

## 6. How scoring works (very important)

### Rule A — Higher is better  
Used for: OEE, PM Compliance, MTBF

```text
Score % = (Actual ÷ Target) × 100
Then if Score > 100, make it 100
```

Example (OEE):

- Target = 82  
- Actual = 78  
- Score = 78 ÷ 82 × 100 = **95.1%**

### Rule B — Lower is better  
Used for: Breakdown Frequency, Breakdown Hours, MTTR

```text
Score % = (Target ÷ Actual) × 100
Then if Score > 100, make it 100
If Actual = 0, Score = 100
```

Example (Breakdown Hours):

- Target = 20  
- Actual = 18  
- Score = 20 ÷ 18 × 100 = 111% → capped to **100%**

### Rule C — Safety

```text
If LTI = 0 → Score = 100%
If LTI > 0 → Score = 0%
```

---

## 7. What is “Weight” and “Weighted contribution”?

Each KPI is not equally important.

Example:

- OEE is 20% of the total  
- Safety is 10% of the total  

**Weighted contribution** = Score × Weight

Example:

- OEE score = 95.1%  
- Weight = 20% = 0.20  
- Weighted = 95.1 × 0.20 = **19.0 points**

At the end, add all 7 weighted points:

```text
OEE + BF + BH + PM + MTTR + MTBF + Safety = Final KPI Score %
(Maximum 100%)
```

Printed example from your company paper:

```text
19.0 + 10.0 + 15.0 + 19.6 + 12.5 + 10.0 + 10.0 = 96.1%
```

---

## 8. How bonus money is calculated

Each job role has a **maximum possible bonus** (called “opportunity”).

Example:

- Maintenance engineer (day shift) opportunity = **£324**  
- Final KPI score = **96.1%**  

```text
Bonus paid = 324 × 96.1% = £311.36
```

In Excel:

```excel
=324 * 96.1 / 100
```

---

## 9. Extra rules that can reduce bonus (gatekeepers)

Even if KPI score is high, bonus can be reduced:

| Situation | What happens to bonus |
|-----------|------------------------|
| Any Lost Time Injury (LTI) | Cut to **50%** |
| Red audit | Cut to **50%** |
| Major safety violation | Bonus becomes **0** |
| Major EPW | Bonus becomes **0** |
| Dishonest / fake reporting | Bonus becomes **0** |
| Green audit | Possible **extra reward** (ask manager the amount) |

---

## 10. How to create the Excel file (step by step)

### Step 1 — Open Excel
Create a blank workbook.

### Step 2 — Make 4 sheets
Rename sheets to:

1. `1_Parameters`  
2. `2_Actuals`  
3. `3_Scorecard`  
4. `4_Bonus`  

**(Easier option:** open the ready file `Excel_Create_KPI_Template.xlsx` instead of building from zero.)

---

## 11. Sheet 1 — Parameters (set once)

This sheet stores the “rules of the game”.

### What you put here

**A. Lines**

| Line code | Machine name |
|-----------|--------------|
| P1 | Pancake machinery |
| T1 | Tortilla wrap machinery |
| T2 | Tortilla wrap machinery |
| L8 | Line L8 |
| L9 | Line L9 |

**B. KPI weights and targets** (copy exactly from scheme)

| KPI | Weight | Year 1 Target |
|-----|--------|---------------|
| OEE | 0.20 | 82 |
| Breakdown Frequency | 0.10 | 15 |
| Breakdown Hours | 0.15 | 20 |
| PM Compliance | 0.20 | 98 |
| MTTR | 0.15 | 2.5 |
| MTBF | 0.10 | 150 |
| Safety | 0.10 | 0 |

**C. Bonus opportunity £** for each role (from scheme paper)

**D. Gatekeeper values** (100% cap, 50% LTI cut, etc.)

> Junior tip: Do **not** change Parameters every month.  
> Only change them if your manager says the scheme changed.

---

## 12. Sheet 2 — Actuals (you fill this every month)

This is your main monthly job.

### Layout

- Column A = name of the data field  
- Column B = where to get it from  
- Columns C–G = P1, T1, T2, L8, L9  

Also type the month in cell **B2**, for example: `2026-07`

### Exact fields you must enter for each line

| # | Field you type | Simple meaning | Where you usually get it |
|---|----------------|----------------|--------------------------|
| 1 | Planned production hours | Hours the line was planned to run | Production plan / Excel |
| 2 | Actual operating hours | Hours it really ran | Line log / Excel |
| 3 | Ideal rate (units/hour) | Perfect speed of the machine | Engineering standard |
| 4 | Actual output units | How many units produced | Production count |
| 5 | Good units | Units that passed quality | Quality / scrap log |
| 6 | Breakdown count | Number of breakdowns | Teams chat + Maintainer |
| 7 | Breakdown hours | Total downtime from breakdowns | Downtime Excel |
| 8 | Planned PM jobs | How many PM jobs were planned | Maintainer system |
| 9 | Completed PM on time | How many finished by due date | Maintainer (completion date) |
| 10 | Operational hours | Running hours used for MTBF | Excel runtime |
| 11 | LTI count | Lost Time Injuries | Health & Safety |
| 12 | Major safety violation (0 or 1) | 0=No, 1=Yes | H&S |
| 13 | Major EPW (0 or 1) | 0=No, 1=Yes | Operations / H&S |
| 14 | Dishonest reporting (0 or 1) | 0=No, 1=Yes | Manager |
| 15 | Audit result | green / amber / red | Audit team |

Paint these input cells **yellow** so you always know “type here”.

---

## 13. Sheet 3 — Scorecard (formulas do the maths)

You should not type answers here. Excel calculates them.

For each line, each KPI has 4 boxes:

1. **Actual** (calculated from Actuals sheet)  
2. **Target** (taken from Parameters sheet)  
3. **Score %** (Actual compared to Target)  
4. **Weighted** (Score × Weight)  

Then at the bottom:

```text
Line KPI Score = sum of all 7 Weighted values
(maximum 100)
```

### One full example for P1 (OEE)

Assume:

- Planned hours = 480  
- Operating hours = 420  
- Ideal rate = 1200  
- Output = 480000  
- Good units = 465600  

Calculate OEE Actual:

```text
Availability = 420 / 480 = 0.875
Performance  = (480000 / 420) / 1200 = 0.9524
Quality      = 465600 / 480000 = 0.97
OEE %        = 0.875 × 0.9524 × 0.97 × 100 ≈ 80.8%
```

Then score:

```text
Score = 80.8 / 82 × 100 ≈ 98.5%
Weighted = 98.5 × 0.20 ≈ 19.7
```

Do the same idea for all other KPIs, then add weighted points.

---

## 14. Sheet 4 — Bonus (final answer for manager)

This sheet should show:

1. Score for P1, T1, T2, L8, L9  
2. Plant score = average of those 5 scores  
3. Gatekeeper checks (LTI, safety, EPW, audit)  
4. Final bonus score %  
5. Money for each job role  

Example:

```text
Plant score = 90.77%
No LTI, no EPW, no red audit
Final bonus score = 90.77%

Maintenance engineer day opportunity = £324
Payout = 324 × 90.77% = £294.09
```

---

## 15. Your monthly routine (checklist)

Every month, do this in order:

1. Ask Production for hours + output for P1, T1, T2, L8, L9  
2. Ask Quality for good units / scrap  
3. Check Teams + Excel for breakdown count and downtime hours  
4. Export PM jobs from Maintainer (planned vs completed on time)  
5. Ask H&S for LTI / major safety / audit colour  
6. Open Excel → go to `2_Actuals` → update yellow cells  
7. Check `3_Scorecard` scores look sensible  
8. Check `4_Bonus` final % and payouts  
9. Save file as `KPI_Report_YYYY-MM.xlsx`  
10. Send to your manager  

---

## 16. Common beginner mistakes

| Mistake | Why it is wrong | Fix |
|---------|-----------------|-----|
| Typing over green formula cells | Breaks calculations | Only type in yellow cells |
| Mixing up Target and Actual | Score becomes nonsense | Target = goal, Actual = real result |
| Using plant total instead of per line for BF/BH | Scheme is per line | Enter each line separately |
| Forgetting Good units ≤ Output | OEE quality becomes >100% | Good units cannot exceed output |
| Changing weights yourself | Scheme is company standard | Ask manager first |
| Ignoring LTI | Bonus may be wrongly high | Always enter safety data |

---

## 17. Which file should you open?

| If you want… | Open this file |
|--------------|----------------|
| Ready template with parameters + formulas | `Excel_Create_KPI_Template.xlsx` |
| Same thing with demo numbers already filled | `Excel_KPI_Calculator.xlsx` |
| This explanation | `docs/JUNIOR_ANALYST_GUIDE.md` |

---

## 18. Tiny practice (do this once)

On P1, enter these practice numbers:

- Planned hours = 480  
- Operating hours = 420  
- Ideal rate = 1200  
- Output = 480000  
- Good = 465600  
- Breakdowns = 12  
- Breakdown hours = 18.5  
- Planned PM = 25  
- PM on time = 24  
- Operational hours = 420  
- LTI = 0  
- Safety flags = 0  
- Audit = green  

Then look at Scorecard:

- You should see OEE around **80.8%**  
- PM = 24/25 = **96%**  
- MTTR = 18.5/12 ≈ **1.54 hours**  
- MTBF = 420/12 = **35 hours**  

If those appear, your sheet is working.

---

## 19. One sentence summary

**You collect Actual monthly data for P1/T1/T2/L8/L9, Excel compares it to fixed Targets, converts each KPI into a weighted score, averages the lines, applies safety rules, and multiplies by each role’s bonus opportunity to get the payout.**

If anything is still unclear, start with only **one line (P1)** and one KPI (**Breakdown Hours**), then add the others one by one.
