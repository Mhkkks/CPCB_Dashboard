# CPCB Air Quality Research Dashboard

A research-oriented dashboard for analyzing:

- PM2.5 variability
- Heat Index variability
- Double diurnal trends
- PM2.5–Heat Index correlation
- Real-time AQI monitoring

using CPCB air quality datasets.

---

# Research Context

This project analyzes:

- Delhi
- Jodhpur

during El Niño periods using hourly CPCB datasets.

The dashboard was developed as part of research presented in:

## URSI-RCRS 2024

---

# Research Abstract

https://www.ursi.org/proceedings/RCRS/2024/RCRS2024_0111.pdf

---

# Features

- PM2.5 Histograms
- Heat Index Histograms
- Double Diurnal Curves
- Correlation Analysis
- Live AQI Cards
- Automatic AQI Refresh (1 hour)
- Sample Dataset Support
- Excel + CSV Support
- Interactive Research Dashboard

---

# Technologies Used

## Frontend

- HTML
- CSS
- JavaScript

## Backend

- FastAPI
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

---

# Folder Structure

\```text
frontend/
backend/

frontend/
├── index.html
├── style.css
├── script.js
├── sample-data/

backend/
├── app/
├── outputs/
\```

---

# How To Run

## Backend

Open terminal inside backend folder:

\```bash
uvicorn main:app --reload
\```

Backend runs at:

\```text
http://127.0.0.1:8000
\```

---

## Frontend

Open terminal inside frontend folder:

\```bash
python -m http.server 5500
\```

Open:

\```text
http://127.0.0.1:5500
\```

---

# How To Download CPCB Data

1. Open CPCB Dashboard:

https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing

2. Click:

\```text
Comparison Data
\```

3. Select:
- One station at a time
- PM2.5
- Temp
- RH
- AT

4. Download hourly datasets in:

\```text
.xlsx
\```

format.

5. Upload datasets into dashboard.

---

# Important Note

Do NOT download multiple stations simultaneously from CPCB comparison export.

It often creates malformed merged columns and missing parameter fields.

Always export one station at a time.

---

# Supported File Formats

- .csv
- .xlsx

---

# Sample Dataset

Sample datasets are included inside:

\```text
frontend/sample-data/
\```

Datasets:
- delhi2019.xlsx
- delhi2023.xlsx
- jodhpur2019.xlsx
- jodhpur2023.xlsx

Use:

\```text
Run Using Sample Dataset
\```

button for demo mode.

---

# AQI API

Current AQI values are fetched using: WAQI API



# Research Outputs

Dashboard generates:

- PM2.5 Histograms
- Heat Index Histograms
- Correlation Analysis
- Double Diurnal Curves

Outputs are stored in:

\```text
backend/outputs/
\```

---

# Future Improvements

- Interactive Plotly Graphs
- CPCB API Integration
- Multi-city comparison
- Temporal anomaly detection

---


