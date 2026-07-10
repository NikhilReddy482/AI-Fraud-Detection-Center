# AI Fraud Intelligence Center 🛡️💼

The **AI Fraud Intelligence Center** is an enterprise-grade banking risk evaluation and real-time fraud mitigation platform. Designed for modern financial networks, it bridges the gap between raw data science and business operations by running a high-accuracy Tri-Model Machine Learning Ensemble alongside a heuristics-based Risk Engine. The platform features an interactive analyst operations queue, advanced data analytics, batch predictions, and a premium dark-themed command center interface.

---

## 🚀 Key Features

* **Tri-Model Ensemble Inference**: Combines unsupervised outlier detection, deep neural reconstruction, and recall-optimized supervised classifiers to flag both historical signatures and zero-day threat patterns.
* **Unified Risk Scoring**: Aggregates model outputs, anomaly scores, and monetary values into intuitive risk profiles, alert priority levels (P1–P4), and automated compliance instructions.
* **Analyst Operations Queue**: A dedicated workspace for case tracking. Fraud managers can assign analysts, change investigation ticket statuses, and log detailed action histories.
* **Live Sandbox & Batch CSV Tool**: Allows investigators to test individual transactions using preloaded templates or run bulk inference on complete dataset files.
* **Interactive Analytics Console**: Visualizes transaction distributions, monthly volumes, anomaly rates, and model performance metrics via dynamic Plotly widgets.
* **Dynamic Theme Switcher**: Repaints the entire application in real time between an Obsidian Dark Mode and a Slate Light Mode.
* **Modular Codebase**: Decoupled, robust structure separating data loading, machine learning computation, business rules, and UI layout elements.

---

## 📊 Machine Learning Pipeline

The detection engine combines three independent models to guarantee high Recall and Precision on highly imbalanced datasets:
1. **HistGradientBoosting Classifier (Supervised)**: Trained on the full transaction set (283,726 rows) to recognize established fraud patterns (**ROC AUC: 0.973, Recall: 81%**).
2. **Deep AutoEncoder (Unsupervised Neural Network)**: Evaluates reconstruction loss to identify zero-day anomalies that deviate from baseline behavior.
3. **Isolation Forest (Unsupervised)**: Employs multi-dimensional, tree-based partitioning to isolate outliers in transaction frequency, amounts, and location profiles.

---

## ⚙️ Project Structure

```text
├── dashboard/
│   ├── app.py                  # Dashboard Entrypoint (Home Hub)
│   ├── assets/
│   │   └── styles.css          # Color Variables, Animations & Layout CSS
│   ├── components/
│   │   ├── sidebar.py          # Sidebar, Navigation & Theme Toggle Widget
│   │   ├── header.py           # Premium Page Title & Header SVG Blocks
│   │   ├── footer.py           # Centralized UI Footer
│   │   ├── metric_cards.py     # Grid Component displaying SVG Metric Cards
│   │   ├── alert_table.py      # Real-time Alert Table View
│   │   ├── system_health.py    # UI Health Checks
│   │   ├── model_health.py     # Latency & Model Status Console
│   │   └── plotly_charts.py    # Analytical Charts Wrapper
│   ├── pages/
│   │   ├── Analytics.py        # Analytics & Filter Dashboard
│   │   ├── Live_Prediction.py  # Manual Templates & Batch CSV Inference
│   │   ├── Fraud_Alerts.py     # Analyst Ticket Operations Console
│   │   ├── Reports.py          # CSV Compliance Export Center
│   │   ├── Performance.py      # Inference Latency & Readiness Dashboard
│   │   └── About.py            # System Architecture & Tech Stack Summary
│   └── utils/
│       ├── predict.py          # Ensemble Inference Loader
│       ├── risk_engine.py      # Scoring Weights & Recommendation Logic
│       ├── helpers.py          # CSS Loader & Theme Overrides Injector
│       └── load_data.py        # Data Caching & Metric Computations
├── data/
│   └── final_dashboard_dataset.csv # Evaluation Transaction Logs (ignored in Git push)
└── models/
    ├── supervised_model.pkl    # Trained HistGradientBoosting weights
    ├── autoencoder_model.h5    # Serialized AutoEncoder weights
    └── isolation_forest.pkl    # Serialized Isolation Forest weights
```

---

## 🛠️ Installation & Execution

### 1. Clone the repository
```bash
git clone https://github.com/NikhilReddy482/fraud-detection-system.git
cd fraud-detection-system
```

### 2. Set up virtual environment
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run dashboard/app.py
```

---

## 💻 Tech Stack

* **Frontend**: Streamlit, Custom HTML5/CSS3 (Glassmorphism & Custom SVG Vectors)
* **Backend**: Python, Pandas, NumPy, Scikit-learn
* **Machine Learning**: TensorFlow (Keras AutoEncoder), HistGradientBoostingClassifier, Isolation Forest
* **Visualization**: Plotly Express, Plotly Graph Objects
* **Styles**: Centralized root variables with real-time CSS injection override tags

---

## 💻 Authors

* **Developer**: Gurrala Nikhil Reddy
