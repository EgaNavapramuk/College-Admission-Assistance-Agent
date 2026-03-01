# College Admission Assistance Agent (India)

Streamlit app that recommends colleges based on:
- Entrance exam rank
- Category + gender cutoff eligibility
- Budget (fee)
- Location (district)

It also includes a lightweight **RAG-style retriever** (local TF‑IDF vector search) to generate a short explanation using the college database context.

## Run locally

### 1) Activate venv (recommended)

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation (ExecutionPolicy), you can either:

- Run commands without activating (recommended):

```powershell
.\venv\Scripts\python -m pip install -r requirements.txt
.\venv\Scripts\python -m streamlit run app.py
```

- Or enable venv activation for the current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Start the app

```powershell
streamlit run app.py
```

## Student preference configuration guide

In the UI, set:
- **Rank**: your entrance rank (smaller is better)
- **Gender**: `BOYS` or `GIRLS` (matches cutoff columns)
- **Category**: `OC`, `SC`, `ST`, `BC_A`… `BC_E`, `EWS` (based on what exists in your dataset)
- **Branch**: select the branch name from the dataset
- **Preferred District**: pick a district or “(Any)”
- **Maximum Fee**: set `0` for no fee limit

## College database integration

This project currently reads `cleaned.xlsx`.

### Required columns (current dataset)
Your Excel should include these (case/spacing can vary; the loader normalizes):
- `INSTITUTE NAME`
- `DISTRICT`
- `BRANCH NAME`
- `FEE`
- Cutoff columns like `OC BOYS`, `OC GIRLS`, `SC BOYS`, `SC GIRLS`, `BC_A BOYS`, ... `EWS GEN OU`, `EWS GIRLS OU`

### Replace the database
1. Replace `cleaned.xlsx` with your own Excel file (same name), or update the path in:
   - `app.py` (calls `load_college_dataset("cleaned.xlsx")`)
   - `recommender.py` / `rag_system.py`
2. Make sure your cutoff columns follow the pattern:
   - `<CATEGORY> _BOYS` / `<CATEGORY> _GIRLS` after normalization

## Project files
- `app.py`: Streamlit UI
- `college_data.py`: dataset loader + column normalization
- `recommender.py`: filtering + scoring + ranking
- `rag_system.py`: local TF‑IDF retrieval + explanation text

