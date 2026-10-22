from pathlib import Path
import csv
import re
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'data' / 'messages.csv'
app = Flask(__name__)

# Small, bundled starter dataset so the project runs without downloading model files.
DEFAULT_DATA = [
    ('ham', 'Hey, are we still meeting for lunch today?'),
    ('ham', 'Your class starts at 9 AM in the usual room.'),
    ('ham', 'Please call me when you reach home.'),
    ('ham', 'Thanks for sharing the notes, they helped a lot.'),
    ('ham', 'Can you send the project report tonight?'),
    ('ham', 'I will be there in ten minutes.'),
    ('ham', 'Happy birthday! Have a wonderful day.'),
    ('ham', 'The meeting has been moved to Friday afternoon.'),
    ('ham', 'Dinner is ready, come downstairs.'),
    ('ham', 'Your appointment is confirmed for tomorrow.'),
    ('spam', 'Congratulations! You have won a free prize. Click now to claim.'),
    ('spam', 'URGENT: Your account is suspended. Verify your password immediately.'),
    ('spam', 'You have been selected for a cash reward. Call this number now.'),
    ('spam', 'Earn money fast from home with no experience required.'),
    ('spam', 'Claim your free gift card today, limited time offer.'),
    ('spam', 'Your package is on hold. Pay a small fee using this link.'),
    ('spam', 'Exclusive loan approved instantly. Apply now.'),
    ('spam', 'You are a lucky winner! Send your bank details to receive money.'),
    ('spam', 'Get cheap medicines and amazing discounts, buy now.'),
    ('spam', 'Final warning: click this link to avoid account closure.'),
    ('spam', 'Investment opportunity guarantees huge profits every week.'),
    ('ham', 'I have attached the assignment file for you.'),
    ('spam', 'Act now to get 90 percent off. Offer expires today.'),
    ('ham', 'Are you coming to college tomorrow?'),
]

def load_dataset():
    if DATA_FILE.exists():
        with DATA_FILE.open('r', encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        valid = [(r.get('label', '').strip().lower(), r.get('message', '').strip()) for r in rows]
        valid = [(label, message) for label, message in valid if label in {'spam', 'ham'} and message]
        if len(valid) >= 4 and len({x[0] for x in valid}) == 2:
            return valid
    return DEFAULT_DATA

def build_model():
    rows = load_dataset()
    texts = [message for label, message in rows]
    labels = [label for label, message in rows]
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, strip_accents='unicode', ngram_range=(1, 2), sublinear_tf=True)),
        ('classifier', MultinomialNB(alpha=0.25)),
    ])
    pipeline.fit(texts, labels)
    return pipeline

model = build_model()

def risk_level(probability):
    if probability >= 0.85:
        return 'High'
    if probability >= 0.60:
        return 'Moderate'
    return 'Low'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    message = ''
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        if message:
            prediction = model.predict([message])[0]
            probabilities = model.predict_proba([message])[0]
            classes = list(model.named_steps['classifier'].classes_)
            spam_probability = float(probabilities[classes.index('spam')])
            confidence = spam_probability if prediction == 'spam' else 1 - spam_probability
            result = {
                'label': prediction,
                'confidence': round(confidence * 100),
                'spam_probability': round(spam_probability * 100),
                'risk': risk_level(spam_probability),
                'words': len(re.findall(r"\b[\w'-]+\b", message)),
            }
    return render_template('index.html', result=result, message=message)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'SpamShield'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
