# ScamShield Pakistan

A beginner-friendly, rule-based scam-warning web application built with Python and Streamlit.

## Requirements
- Python 3.11+
- Internet connection for first-time package installation

## Setup on Windows
Open a terminal in this project folder and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, you can use Command Prompt:

```bat
.venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run app.py
```

## Run tests
```powershell
python -m unittest discover -s tests
```

## Academic concepts
- OOP: `ScamAnalyzer` class and storage functions
- Discrete Structures: Boolean rule checks and feature sets
- Linear Algebra: binary feature vector and weighted sum (conceptual formulation)
- Basic Mathematics: sum and capped score thresholds
- Probability Distributions: future extension for analyzing frequencies in a labeled dataset

## Limitations
The score is a heuristic, not a probability of fraud. No URLs are opened or fetched. A low score does not establish that a message is safe. History is stored locally and includes a short message preview; do not enter real sensitive information.
