from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import joblib
from utils import extract_keywords
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Limit max file size (2MB)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['resume_checker']
collection = db['submissions']

model = joblib.load("resume_model.pkl")

REQUIRED_KEYWORDS = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning",
    "Data Science", "SQL", "Django", "Flask", "HTML", "CSS", "JavaScript",
    "Git", "GitHub", "React", "Node.js", "Communication", "Teamwork", "Leadership"
]

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        ptext = page.extract_text()
        if ptext:
            text += ptext
    return text

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Max size is 2MB."}), 413

@app.route("/upload", methods=["POST"])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        text = extract_text_from_pdf(file)
    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 400

    if not text.strip():
        return jsonify({"error": "No text found in PDF"}), 400

    found = extract_keywords(text, REQUIRED_KEYWORDS)
    missing = list(set(REQUIRED_KEYWORDS) - set(found))

    pred = model.predict([text])[0]
    proba = max(model.predict_proba([text])[0])

    score = round(len(found) / len(REQUIRED_KEYWORDS) * 100)

    collection.insert_one({
        "filename": file.filename,
        "score": score,
        "found_keywords": found,
        "missing_keywords": missing,
        "prediction": int(pred),
        "confidence": float(proba)
    })

    return jsonify({
        "score": score,
        "found": found,
        "missing": missing,
        "prediction": int(pred),
        "confidence": round(proba * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
