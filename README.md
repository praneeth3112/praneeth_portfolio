# Praneeth Reddy Kadavakolla — AI/ML Portfolio

Personal portfolio showcasing AI/ML, Python, and interactive web projects, paired with a Python/Flask API and validation suite.

## Live Site
- Portfolio: https://portfolio-praneethreddy.netlify.app

## Stack
- **Python**: `portfolio_data.py`, `app.py` (Flask + stdlib HTTP API), `build.py` (validator & analyzer), `tests/test_portfolio.py`
- **Frontend**: React, TypeScript, Vite, Tailwind CSS (`src/App.tsx`)

## Running Locally

### Python API & Tests
```bash
python3 build.py
python3 -m unittest discover -s tests -v
python3 app.py
```

### Frontend (Vite)
```bash
npm install
npm run dev
```
