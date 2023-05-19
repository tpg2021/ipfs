import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load pre-trained spaCy models
nlp = spacy.load('en_core_web_sm')

# Define regular expressions for different mortgage types
fha_regex = r'\bFHA\b|\bFederal Housing Administration\b'
va_regex = r'\bVA\b|\bVeterans Administration\b'
conventional_regex = r'\bconventional\b'
hba_regex = r'\bHBA\b|\bHome Buyers Assistance\b'


# Define function to preprocess text
def preprocess_text(text):
    # Remove newlines and tabs
    text = re.sub(r'\s+', ' ', text)
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text


# Define function to extract features from text using TF-IDF
def extract_features(text):
    # Preprocess text
    text = preprocess_text(text)
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    # Fit vectorizer to text
    vectorizer.fit_transform([text])
    # Return feature matrix
    return vectorizer.transform([text])


# Define function to predict mortgage type
def predict_mortgage_type(text):
    # Extract features from text
    features = extract_features(text)
    # Load pre-trained Naive Bayes models
    model = MultinomialNB()
    model.fit(features, ['FHA', 'VA', 'conventional'])
    # Make prediction
    prediction = model.predict(features)[0]
    return prediction


# Define function to parse PDF text using spaCy
def parse_pdf_text(pdf_file):
    # Load PDF file
    with open(pdf_file, 'rb') as f:
        pdf_text = f.read()
    # Convert PDF text to Unicode
    pdf_text = pdf_text.decode('utf-8', errors='ignore')
    # Remove page numbers and other extraneous text
    pdf_text = re.sub(r'\d+ of \d+', '', pdf_text)
    pdf_text = re.sub(r'continued on next page', '', pdf_text)
    # Parse text using spaCy
    doc = nlp(pdf_text)
    # Extract relevant sentences
    relevant_sentences = []
    for sentence in doc.sents:
        if re.search(fha_regex, sentence.text) or re.search(va_regex, sentence.text) or \
                re.search(conventional_regex, sentence.text) or re.search(hba_regex, sentence.text):
            relevant_sentences.append(sentence.text)
    # Join relevant sentences into a single string
    relevant_text = ' '.join(relevant_sentences)
    return relevant_text


# Example usage
input_file = 'HBA-Mortgage-form.pdf'
pdf_text = parse_pdf_text(input_file)
mortgage_type = predict_mortgage_type(pdf_text)
print(f'The PDF file is a {mortgage_type} mortgage file.')
