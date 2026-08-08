# Connect Dashboard to Excel + Refresh automatically

## What you asked for
When you open/click **Dashboard** and press **Refresh**, latest data should load into scores and charts.

---

## Use this file
`Excel_Dashboard_Connected_Refresh.xlsx`

Sheets:
| Sheet | Role |
|-------|------|
| **Source_Data** | Type/paste monthly numbers (yellow). Table name: `KPI_Source` |
| **Calc** | Score + Weighted (connected by formulas) |
| **Dashboard** | Manager view (cards, table, chart) |
| **How_To_Connect_Refresh** | Instructions |

---

## Method A — same Excel file (recommended for you)

### Connection
Dashboard cells use formulas like:
```excel
=Source_Data!B2
=Calc!Q9
=Calc!Q3
```

So Dashboard is already connected to the Excel data sheet.

### Refresh steps
1. Update yellow cells on **Source_Data**
2. Click **Dashboard**
3. Press **`Ctrl + Alt + F5`**  
   or ribbon: **Data → Refresh All**
4. Scores + chart reload

### Make formulas always auto-calculate
**File → Options → Formulas → Workbook Calculation → Automatic**

With Automatic on, numbers update as soon as Source_Data changes.  
Refresh All is still useful for charts/queries.

---

## Method B — Dashboard connected to a different Excel file

Use this if operators type data in one file, and you show a separate Dashboard file.

1. Open your **Dashboard** workbook  
2. **Data → Get Data → From File → From Workbook**  
3. Select the source Excel (the file with P1/T1/T2 data)  
4. Pick the sheet/table → **Load** (or Load to Table)  
5. Point Dashboard cards/charts to that loaded table  
6. Every time you need latest data:  
   **Data → Refresh All**

### Refresh when file opens
1. **Data → Queries & Connections**
2. Right-click your query → **Properties**
3. Tick **Refresh data when opening the file**
4. Optional: Tick **Refresh every 60 minutes**

---

## Method C — Power BI dashboard

If your “dashboard” is Power BI (not Excel):

1. Power BI Desktop → **Get data → Excel workbook**
2. Select `Source_Data` / table `KPI_Source`
3. Build visuals
4. **Publish** to Power BI service
5. Click **Refresh** in Power BI (or schedule refresh)

---

## Keyboard / buttons

| Action | How |
|--------|-----|
| Refresh All | `Ctrl + Alt + F5` |
| Ribbon refresh | Data → Refresh All |
| Auto on open | Query Properties → Refresh when opening |

---

## Test (2 minutes)
1. `Source_Data` → change P1 OEE `C5` to `90`
2. `Dashboard` → `Ctrl + Alt + F5`
3. Plant Score and P1 score should rise  
4. Change it back after the test

---

## Rules
- Type data **only** on Source_Data  
- Never type over green Dashboard formulas  
- Keep table name `KPI_Source` if using Power Query  
- One source → one dashboard connection
