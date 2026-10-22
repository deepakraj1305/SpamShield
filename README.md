# 🛡️ SpamShield — Smart Message Spam Detector

**SpamShield** is a machine-learning web application that screens SMS messages and short text for likely spam. It combines natural language processing (NLP), TF-IDF feature extraction, and a Multinomial Naive Bayes classifier with a responsive, dark security-inspired interface.

> **Important:** This repository contains an educational demonstration model trained on a small sample dataset. Its confidence values are model estimates, not verified real-world accuracy. Do not rely on it as the sole method for identifying scams.

## ✨ Features

- Real-time classification of a message as **potential spam** or **likely legitimate**
- Spam probability and prediction confidence estimates
- Risk indicator and word count
- TF-IDF word and bigram features with a Multinomial Naive Bayes classifier
- Responsive interface with sample messages and live character count
- Local `/health` endpoint for basic service checks
- No database; the app does not intentionally persist submitted messages

## 🧰 Tech stack

- Python 3.10+
- Flask
- scikit-learn (TF-IDF + Multinomial Naive Bayes)
- HTML, CSS, JavaScript

## 📁 Project structure

```text
SpamShield/
├── app.py                 # Flask app and ML prediction pipeline
├── requirements.txt       # Python dependencies
├── Procfile               # Gunicorn start command for compatible hosts
├── README.md
├── .gitignore
├── data/
│   └── messages.csv       # Small example training dataset
├── models/                # Reserved for optional saved model artifacts
├── templates/
│   └── index.html         # Web interface
└── static/
    ├── style.css          # Responsive visual design
    └── script.js          # Example messages and character counter
```

## 🚀 Run locally (Windows PowerShell)

1. Install Python 3.10 or newer.
2. Open PowerShell in the project folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python app.py
   ```

6. Open **http://127.0.0.1:5000** in your browser.

On macOS/Linux, activate the environment with `source .venv/bin/activate`.

## ☁️ Deployment

This is a Python/Flask application, not a static frontend. Deploy it to a Python-capable host (for example, Render or Railway) rather than deploying it as a static-only Vercel site.

For a typical host:

- **Build/install command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`
- **Health check path (optional):** `/health`
- **Python version:** 3.10 or newer

Set the Python version using your host's supported configuration method if needed. Do not commit secrets or environment files.

## 🧠 How it works

1. The app loads labelled examples from `data/messages.csv`; if the file is missing or invalid, it falls back to bundled starter examples.
2. `TfidfVectorizer` transforms text into weighted word and bigram features.
3. `MultinomialNB` learns patterns from the labelled examples and predicts `spam` or `ham`.
4. The UI displays the class estimate, model confidence, and spam probability.

### Add more training examples

Edit `data/messages.csv` using this format:

```csv
label,message
ham,"Your class starts at 9 AM."
spam,"You won a prize, click to claim now!"
```

Allowed labels are `ham` and `spam`. Restart the application after updating the CSV so the model is retrained. Use a large, representative, correctly labelled dataset before evaluating model performance. For a credible evaluation, use a held-out test set and report precision, recall, F1-score, and a confusion matrix.

## 🔐 Privacy and limitations

- This demo does not store submitted messages in a database or write them to application files. Hosting providers may still collect standard request logs.
- Predictions depend on the limited training examples and can be wrong, including false positives and false negatives.
- Do not paste passwords, OTPs, bank details, or other sensitive information into demo apps.
- A model classification is not proof that a message is safe or malicious. Verify sender identity and URLs independently.

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Open a pull request with a clear description.

## 📄 License

Choose a license before distributing the project publicly. If you use a dataset or model from another source, preserve its license and attribution requirements.

---

**Project name:** SpamShield — Smart Message Spam Detector  
**Category:** Machine Learning · NLP · Web Application
