# How to create a KPI Dashboard (junior guide)

You need **3 sheets** in Excel:

1. **Data** — type monthly numbers  
2. **Calc** — formulas for Score + Weighted  
3. **Dashboard** — what your manager sees (cards + table + charts)

Ready file: `Excel_KPI_Dashboard.xlsx`

---

## Step-by-step (create yourself)

### Step 1 — Create sheets
Rename sheets to: `Data`, `Calc`, `Dashboard`

### Step 2 — Data sheet
Make a table like this:

| Line | Name | OEE % | BF | BH | PM % | MTTR | MTBF | LTI |
|------|------|-------|----|----|------|------|------|-----|
| P1 | Pancake | | | | | | | |
| T1 | Tortilla | | | | | | | |
| T2 | Tortilla | | | | | | | |
| L8 | Line L8 | | | | | | | |
| L9 | Line L9 | | | | | | | |

Also store Targets + Weights (OEE 82 / 20%, etc.).

Paint input cells **yellow**.

### Step 3 — Calc sheet (Score + Weighted)
For each line and each KPI:

**Score**
- Higher better: `=MIN(100, Actual/Target*100)`
- Lower better: `=IF(Actual=0,100,MIN(100,Target/Actual*100))`
- Safety: `=IF(LTI=0,100,0)`

**Weighted**
```excel
=Score * Weight
```

**Total**
```excel
=MIN(100, SUM of 7 Weighted)
```

**Plant score**
```excel
=AVERAGE of P1,T1,T2,L8,L9 totals
```

### Step 4 — Dashboard sheet layout

```text
Row 1:  Title — Signature Flatbreads Maintenance KPI Dashboard
Row 2:  Month | Plant Score % | Bonus £
Row 4:  6 KPI cards (OEE, BF, BH, PM, MTTR, MTBF)
Row 10: Table — Line scores + status
Row 28: Charts
```

### Step 5 — Add charts
1. Select Line + Total Score  
2. **Insert → Charts → Column chart**  
3. Title: “Total KPI Score % by Line”  
4. Add second chart: Actual vs Target  
5. Add third chart: Weighted points by KPI  

### Step 6 — Add colours
Select Total Score column →  
**Home → Conditional Formatting → Colour Scales**  
(red = low, green = high)

### Step 7 — Status formula
```excel
=IF(Total>=90,"Good",IF(Total>=80,"OK","Needs focus"))
```

### Step 8 — Monthly use
Every month:
1. Update yellow cells on **Data**
2. Open **Dashboard**
3. Show manager

Do **not** rebuild charts each month.

---

## What a good dashboard shows

| Area | Purpose |
|------|---------|
| Big plant score | One number for the month |
| KPI cards | Quick health check |
| Line table | Which machine needs help |
| Bar chart by line | Visual comparison |
| Actual vs Target | Gap to goal |
| Safety flag | Pass/Fail for LTI |

---

## Tips for your factory

- Keep Dashboard to **one screen**
- Max **3 charts**
- Use machine names managers know: Pancake, Tortilla, L8, L9
- Hide the Calc sheet before presenting (right-click tab → Hide)
- Save each month as `KPI_Dashboard_2026-07.xlsx`
