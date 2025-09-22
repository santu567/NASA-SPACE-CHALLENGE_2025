<div align="center">

# 🚀 NASA Space Challenge 2025 — City Growth Impact Prototype

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-004B6E)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-informational)](#license)

<strong>Draw. Predict. Compare.</strong> Model how city development affects local climate — in seconds.

</div>

---

### ✨ What is this?
An interactive geospatial web app that lets you draw areas on a map, simulate development vs. park scenarios, and get AI-powered predictions of temperature change (ΔLST) with rich visualizations. Built for the NASA Space Apps Challenge 2025.

- **Interactive mapping** with drawing tools (Folium)
- **Environmental metrics** (NDVI, LST, AOD, area)
- **AI predictions** using a trained XGBoost model
- **Scenario comparison**: Development vs. Park with impact scores
- **One‑click export** of GeoJSON and results

---

### 🔗 Live Demo
If deployed on Streamlit Cloud, your app URL goes here:

`https://nasa-space-challenge2025.streamlit.app` (placeholder)

---

### 🧠 Core Features
- **Draw & analyze**: Sketch polygons, compute area, centroid, and spatial metrics
- **Multi‑city baselines**: New Delhi, San Francisco, Nairobi
- **Scenario modeling**: Tune parameters and instantly compare outcomes
- **AI engine**: ΔLST prediction + feature importance
- **Visual dashboard**: Charts, tables, and metrics that update live
- **Export**: Download drawn shapes as GeoJSON and results for analysis

See full details in `FEATURES.md` and a condensed overview in `QUICK_FEATURES.md`.

---

### 🏗️ Architecture (High Level)
```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                FRONTEND (Streamlit)                             │
│  • Folium map + drawing tools • Controls • Live charts • Exports                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATA PROCESSING & RULES                               │
│  • Shapely geometry • NDVI • LST • AOD • Impact score (0–100)                   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               MACHINE LEARNING                                   │
│  • XGBoost regression • Feature engineering • Real‑time inference                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                STORAGE & MODELS                                  │
│  • models/xgb_model.joblib • requirements/runtime • versioning                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

More details in `ARCHITECTURE.md`.

---

### 🧰 Tech Stack
- **Frontend**: Streamlit, Folium, Matplotlib
- **Backend**: Python 3.13, Pandas, NumPy, Shapely
- **ML**: XGBoost 2.0.3, scikit‑learn, joblib
- **Deployment**: Streamlit Cloud (optional), Git

---

### ⚡ Quickstart

1) Clone and enter the project
```bash
git clone <your-repo-url>
cd nasa_space
```

2) Create a virtual environment (recommended) and install deps
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3) Run the app
```bash
streamlit run app.py
```

4) Open your browser at `http://localhost:8501`

---

### 🕹️ Usage
1. Choose a baseline city in the control panel.
2. Draw a polygon on the map to select your area of interest.
3. Adjust scenario parameters (Development vs. Park) as needed.
4. View AI predictions (ΔLST), impact scores, and visual comparisons.
5. Export your shapes and results for further analysis.

---

### 📁 Project Structure
```text
nasa_space/
├─ app.py                   # Streamlit app entrypoint
├─ models/
│  └─ xgb_model.joblib      # Trained XGBoost model
├─ train_xgb.py             # Script to generate/train the model
├─ requirements.txt         # Python dependencies
├─ runtime.txt              # Python runtime version
├─ FEATURES.md              # Comprehensive feature list
├─ QUICK_FEATURES.md        # Fast reference of capabilities
└─ ARCHITECTURE.md          # System design and data flow
```

---

### 🤖 Model Details
- Regression model trained on synthetic environmental data (~3,000 samples)
- Predicts temperature change (ΔLST) given geospatial and environmental features
- Persisted to `models/xgb_model.joblib` and cached at runtime for fast inference
- Displays feature importance for transparency and explainability

To retrain locally:
```bash
python train_xgb.py
```

---

### 🗺️ Roadmap
- NASA satellite data integration (Landsat/MODIS) via GEE
- Multi‑temporal analysis and richer visualizations
- Public API endpoints and data export formats
- Mobile‑responsive layout improvements

---

### 🤝 Contributing
Pull requests are welcome! If you plan a large change, please open an issue to discuss approach and scope first.

---

### 📜 License
This project is released under the MIT License — free to use, modify, and share.


