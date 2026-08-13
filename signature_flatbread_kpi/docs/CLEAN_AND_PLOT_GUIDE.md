# Clean 17,000-row data and plot graphs (junior guide)

## Your goal
1. Clean huge Excel/CSV data (~17,000 rows)  
2. Plot graphs for manager  

## Ready demo
Sample messy file (17,120 rows):  
`data/raw/plant_events_17k_SAMPLE.csv`

Run:
```bash
cd signature_flatbread_kpi
python scripts/clean_and_plot.py
```

Outputs:
- Cleaned data → `data/cleaned/..._CLEANED.csv`
- Graphs → `plots/*.png`
- Report → `data/cleaned/..._CLEANING_REPORT.txt`

---

## Use YOUR real 17k file

1. Copy your file into:
   `signature_flatbread_kpi/data/raw/your_data.csv`
2. Run:
```bash
python scripts/clean_and_plot.py --input data/raw/your_data.csv
```

---

## What cleaning does

| Step | Why |
|------|-----|
| Fix column names | Remove spaces / weird characters |
| Trim text | `" p1 "` → `P1` |
| Fix dates | Text → real dates |
| Convert numbers | `"12.5"` → 12.5 |
| Remove empty rows | Useless blanks |
| Remove duplicates | Same row twice |
| Fix bad values | Negative downtime, Good > Output |
| Fill missing | Median for numbers, `"Unknown"` for text |
| Cap extreme outliers | Stops 999-hour errors from breaking charts |

---

## Graphs created

1. Records by Line (P1/T1/T2/L8/L9)  
2. Total downtime by Line  
3. Event type mix (pie)  
4. Daily downtime trend  
5. Output vs Good units  

---

## Clean in Excel (if you prefer Excel)

1. Open CSV in Excel  
2. **Data → Remove Duplicates**  
3. Use **Filter** to find blanks  
4. **Text to Columns** / format dates  
5. Fix Line names with Find/Replace (`p1` → `P1`)  
6. Select data → **Insert → Charts**  

For 17k rows, Python is faster and safer.

---

## Important
I did not find your real 17k file in the project yet.  
Put it in `data/raw/` and re-run the script.
