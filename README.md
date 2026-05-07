# 🇮🇳 India 360° Travel AI — Django Web Application

> Production-grade Django + HTML/CSS frontend for the India 360° Travel AI ML system.
> Powered by 13 specialized XGBoost / LightGBM models.

---

## 📁 Project Structure

```
india360/
├── manage.py
├── requirements.txt
├── india_360_travel_ai_dataset.csv     ← Drop your dataset here
├── models_dir/                         ← Drop trained .pkl files here
│   ├── manifest.json
│   ├── M01_route_distance.pkl
│   ├── M02_weather.pkl
│   ├── M03_risk.pkl
│   ├── M04_crowd.pkl
│   ├── M05_transport.pkl
│   ├── M06_cost_total.pkl
│   ├── M07_travel_time.pkl
│   ├── M08_best_days.pkl
│   ├── M09_duration.pkl
│   ├── M10_experience.pkl
│   ├── M11_recommendation.pkl
│   ├── M12_ranking.pkl
│   ├── M13_confidence_engine.pkl
│   ├── label_encoders.pkl
│   ├── le_risk.pkl
│   ├── le_transport.pkl
│   └── le_final.pkl
│
├── india360/                           ← Django project package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── travel_ai/                          ← Django app
    ├── ai_engine.py                    ← Core ML inference engine
    ├── views.py                        ← Page + API views
    ├── urls.py                         ← URL routing
    ├── apps.py
    ├── templates/travel_ai/
    │   ├── base.html                   ← Shared layout
    │   ├── index.html                  ← Predict Trip page
    │   ├── recommend.html              ← Top-N Recommendations
    │   └── about.html                  ← AI System info
    └── static/travel_ai/
        ├── css/main.css                ← Full responsive stylesheet
        └── js/
            ├── main.js                 ← Shared utilities
            ├── predict.js              ← Predict page logic
            └── recommend.js            ← Recommend page logic
```

---

## 🚀 Quick Start

### 1. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Place your dataset and models

```bash
# Copy your dataset CSV to the project root
cp /path/to/india_360_travel_ai_dataset.csv .

# Copy your trained model .pkl files
cp /path/to/models/* models_dir/
```

> **No dataset?** No problem — the app runs in **Demo Mode** using a built-in
> synthetic dataset with 15 popular Indian destinations.

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Collect static files (production) / run dev server

```bash
# Development
python manage.py runserver

# Production
python manage.py collectstatic
gunicorn india360.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

Open: **http://127.0.0.1:8000**

---

## 🌐 Pages

| URL | Description |
|-----|-------------|
| `/` | Trip Prediction — enter source/destination, get full AI analysis |
| `/recommend/` | Top-N Destination Recommendations with filters |
| `/about/` | AI system architecture, model details, API reference |

## 📡 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/health/` | System health check |
| `POST` | `/api/predict/` | Single destination prediction |
| `GET` | `/api/recommend/` | Top-N recommendations |
| `GET` | `/api/destinations/` | Full destinations list |

### Example — POST /api/predict/

```json
{
  "source": "Delhi",
  "destination": "Manali",
  "month": 12,
  "budget": "mid",
  "purpose": "adventure",
  "group_type": "couple"
}
```

### Example — GET /api/recommend/

```
/api/recommend/?month=5&budget=luxury&purpose=romantic&group_type=couple&top_n=5
```

---

## ⚙️ Configuration

All settings are in `india360/settings.py`:

```python
MODELS_DIR = BASE_DIR / 'models_dir'      # Change path if needed
DATA_PATH  = BASE_DIR / 'india_360_travel_ai_dataset.csv'
```

For **Redis caching** (recommended for production):

```python
pip install django-redis redis

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

---

## 🧠 ML Inference Modes

| Mode | When | Behaviour |
|------|------|-----------|
| **Full ML** | All 13 .pkl files present | Runs all models sequentially, returns calibrated predictions |
| **Demo** | No .pkl files / manifest.json missing | Uses dataset-derived heuristic predictions — still fully functional |

---

## 🛠️ Tech Stack

- **Backend**: Django 5, Python 3.10+
- **ML**: XGBoost, LightGBM, Scikit-learn, SHAP, Optuna, MLflow
- **Frontend**: Pure HTML5 · CSS3 · Vanilla JavaScript (no frameworks)
- **Fonts**: Inter + Playfair Display (Google Fonts)
- **Cache**: Django LocMemCache (Redis-ready)
