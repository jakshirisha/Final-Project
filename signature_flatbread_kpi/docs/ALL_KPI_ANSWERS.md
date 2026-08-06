# All KPI calculations (with answers)

Open Excel file: `Excel_All_KPI_Calculations.xlsx`

---

## Formulas (copy these)

| KPI | Actual | Score % (max 100) | Weighted |
|-----|--------|-------------------|----------|
| **OEE** | Avail × Perf × Qual × 100 | Actual/82×100 | Score×20% |
| **Breakdown Frequency** | Breakdown count | 15/Actual×100 | Score×10% |
| **Breakdown Hours** | Breakdown hours | 20/Actual×100 | Score×15% |
| **PM Compliance** | Done on time ÷ Planned × 100 | Actual/98×100 | Score×20% |
| **MTTR** | Breakdown hours ÷ count | 2.5/Actual×100 | Score×15% |
| **MTBF** | Operating hours ÷ count | Actual/150×100 | Score×10% |
| **Safety** | LTI count | If 0 → 100, else 0 | Score×10% |
| **TOTAL** | — | Sum of weighted | max 100% |

- Availability = Actual operating time ÷ Planned production time  
- Performance = Actual production rate ÷ Ideal production rate  
  (or `(Total units ÷ Operating time) ÷ Ideal rate`)  
- Quality = Good units ÷ Total units  

For lower-is-better KPIs: if Actual = 0, Score = 100.

---

## Sample answers (July demo data)

### Actual values

| KPI | P1 | T1 | T2 | L8 | L9 |
|-----|----|----|----|----|-----|
| OEE % | 80.83 | 77.58 | 80.65 | 85.07 | 76.34 |
| Breakdown Frequency | 12 | 14 | 11 | 9 | 16 |
| Breakdown Hours | 18.5 | 19.0 | 16.0 | 14.0 | 22.0 |
| PM Compliance % | 96.00 | 96.67 | 96.43 | 100.00 | 90.00 |
| MTTR hours | 1.54 | 1.36 | 1.45 | 1.56 | 1.38 |
| MTBF hours | 35.00 | 28.57 | 37.27 | 48.33 | 24.38 |
| Safety LTI | 0 | 0 | 0 | 0 | 0 |

### TOTAL score %

| Line | Total KPI Score |
|------|-----------------|
| P1 Pancake | **91.64%** |
| T1 Tortilla | **90.56%** |
| T2 Tortilla | **91.83%** |
| L8 | **93.22%** |
| L9 | **86.62%** |
| **Plant average** | **90.78%** |

Example bonus (Maint eng opportunity £324):  
`324 × 90.78% = £294.13`

---

## P1 worked example (hand calculation)

Inputs: Plan 480, Op 420, Ideal 1200, Output 480000, Good 465600, BD 12, BD hrs 18.5, PM 24/25, LTI 0

1. **OEE** = (420/480) × ((480000/420)/1200) × (465600/480000) × 100 = **80.83%**  
   Score = 80.83/82×100 = **98.57%** → Weighted **19.71**
2. **BF** = 12 → Score = min(100, 15/12×100) = **100%** → Weighted **10.00**
3. **BH** = 18.5 → Score = min(100, 20/18.5×100) = **100%** → Weighted **15.00**
4. **PM** = 24/25×100 = **96%** → Score = 96/98×100 = **97.96%** → Weighted **19.59**
5. **MTTR** = 18.5/12 = **1.54h** → Score = min(100, 2.5/1.54×100) = **100%** → Weighted **15.00**
6. **MTBF** = 420/12 = **35h** → Score = 35/150×100 = **23.33%** → Weighted **2.33**
7. **Safety** = 0 LTI → **100%** → Weighted **10.00**

**P1 TOTAL = 19.71+10+15+19.59+15+2.33+10 = 91.63%** (≈91.64%)
