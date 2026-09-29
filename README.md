# Spotify Review Sentiment Analysis
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


An end-to-end data engineering pipeline and interactive NLP web dashboard for scraping, normalizing, and classifying Spotify customer feedback from Trustpilot.

Spotify Review Sentiment Analysis processes raw, multi-page customer feedback from Trustpilot into cleaned tabular datasets, evaluates class-imbalanced ML classifiers, and exposes live inference alongside interactive visual analytics.

## Features
- Anti-Bot Web Scraping: Automated multi-page extraction via Playwright and BeautifulSoup maintaining active browser sessions to bypass Cloudflare and HTTP 403 blocks.

- Text Normalization: Lowercasing, regex-based noise and punctuation removal, token whitespace trimming, and duplicate review elimination.

- Ground Truth Labeling: Automated mapping of user star ratings (1–5) into standardized target labels (Negative, Neutral, Positive).

- Supervised Machine Learning: Feature extraction using TfidfVectorizer (unigrams and bigrams) trained on LogisticRegression with class-weight balancing.

- Hybrid Inference Architecture: Combines global statistical batch analytics with real-time VADER lexicon scoring for arbitrary single-text inputs.

- Interactive Web Analytics: Executive KPI indicators, Plotly distribution bar/pie charts, paginated data inspection, and a live prediction sandbox.

## Architecture
```
  [ Trustpilot Site ]
           │
           │ (Playwright Browser Session)
           │
           ▼
  [ Multi-Page Collector ] ──> (BeautifulSoup Parsing)
           │
           ▼
  [ data/raw_reviews.csv ]
           │
           │ (Regex Cleaning & Normalization)
           │
           ▼ 
  [ Data Preprocessor ]
           │
           ├──> [ TF-IDF + Logistic Regression ] ──> (Classification Metrics)
           │
           ▼
  [ data/processed_reviews.csv ]
           │
           ▼
  [ Streamlit Dashboard ] <── (Plotly Visualizations & Live VADER Sandbox)
```
The application separates offline data ingestion and vectorizer training from frontend web visualization, allowing reproducible execution of each stage.

## Pipeline & Scoring Methodology
### Ground Truth Mapping

Ratings collected from Trustpilot are normalized into target sentiment labels according to the following deterministic rules:

| User Rating  |  Mapped Label | Description                                             |
|:--------------:|:--------------:|:---------------------------------------------------------:|
| 1-2 Stars    |  `Negative`   | Expresses user dissatisfaction, bug reports, or billing issues.|
| 3 Stars      |  `Neutral`    | Mixed sentiment or feature requests without clear polarity.|
| 4-5 Stars    |  `Positive`   | High user satisfaction or praise for core features. |

### Classification Model Performance

Due to natural platform bias on Trustpilot (over 90% negative reviews), the supervised `LogisticRegression` pipeline uses `class_weight='balanced'` and is evaluated using precision, recall, and F1-score:

| Sentiment Class |  Precision | Recall  | F1-Score  |
|:--------------:|:--------------:|:--------:|:------:|
|  `Negative`   | 0.98 |  0.95  | 0.96 |
|  `Neutral`    | 0.40 | 0.50 | 0.44 |
|  `Positive`   | 0.85 | 0.80 | 0.82 |

## Requirements
- Python 3.10 or higher

- Playwright Chromium Browser binaries

- NLTK Vader Lexicon package

## Quick Start
### 1. Clone the repository
```bash
git clone https://github.com/saveriobutright/sentiment-review-analyzer.git
cd sentiment-review-analyzer
```

### 2. Set up Virtual Environment & Dependencies
On Windows Powershell:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```
On macOS or Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```
### 3. Run Ingestion and Preprocessing
Scrape multi-page review data:
```bash
python src/scraper.py
```
Clean text and train ML models:
```bash
python src/nlp_processor.py
```
### 4. Launch the Dashboard
```bash
streamlit run app.py
```
The web dashboard will be available at `http://localhost:8501`.

## Run the Tests
Execute the automated test suite using `pytest`:
  
On Windows PowerShell:
  ```powershell
  pytest
  ```

On macOS or Linux:
```bash
pytest
```

The test suite covers:
- Text normalization and whitespace stripping;

- Regex punctuation and special character removal;

- Lowercase conversion consistency;

- Label mapping logic from user ratings;

- VADER lexicon inference response structure.

## Project Structure
```
.
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── data/
│   ├── raw_reviews.csv
│   └── processed_reviews.csv
├── docs/
│   └── images/
│       └── dashboard_preview.png
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   └── nlp_processor.py
└── tests/
    └── test_nlp.py
```
## Data Source and Attribution
Review data is retrieved live from publicly accessible pages on [Trustpilot](https://www.trustpilot.com/). This project is intended solely for educational, research, and portfolio demonstration purposes.

## Roadmap
- [x] Multi-page automated scraper with Playwright anti-bot handling

- [x] Text normalization and regex cleaning pipeline

- [x] Ground-truth rating-to-label mapping

- [x] TF-IDF feature extraction with bigrams

- [x] Supervised Logistic Regression classification with class balancing

- [x] Streamlit web dashboard with executive KPI cards and Plotly charts

- [x] Hybrid inference sandbox using VADER for single-text inputs

- [x] Pytest automated test coverage for core NLP utility functions

## Releases
The current stable release is v1.0.0

## License

JobRadar is available under the [MIT License](LICENSE).

## Author

**Saverio Polito**

- [GitHub](https://github.com/saveriobutright)
- [LinkedIn](https://www.linkedin.com/in/saverio-polito-a407a53ba)
