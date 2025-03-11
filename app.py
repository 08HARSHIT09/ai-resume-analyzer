from flask import Flask, render_template, request, jsonify
import PyPDF2
import re
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def analyze_resume(text):
    keywords = ["Python", "Machine Learning", "Data Analysis", "Flask", "API", "NLP", "Deep Learning"]
    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    missing_keywords = list(set(keywords) - set(found_keywords))
    
    score = int((len(found_keywords) / len(keywords)) * 100)
    return score, missing_keywords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    text = extract_text_from_pdf(file_path)
    score, missing_keywords = analyze_resume(text)

    return jsonify({"score": score, "missing_keywords": missing_keywords})

if __name__ == '__main__':
    app.run(debug=True)
