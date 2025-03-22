import pickle
import validators
from src.pipeline.predict_pipeline import PredictPipeline

# Load the trained ML model
with open('rf.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize the prediction pipeline
pred = PredictPipeline()

def check_malicious_url(url):
    """
    Checks if a given URL is malicious using the ML model.

    Args:
        url (str): The URL to check.

    Returns:
        str: The classification label (Benign, Defacement, Malware, Phishing).
    """

    if not validators.url(url):
        return "Invalid URL"

    url_input = url.replace('https://', '').replace('http://', '')
    
    # Transform URL using the ML pipeline
    transform_url = pred.transformURL(url_input)

    # Make prediction
    prediction = model.predict([transform_url])[0]

    # Mapping predictions to labels
    labels = {
        0: "Benign",
        1: "Defacement",
        2: "Malware",
        3: "Phishing"
    }
    
    return labels.get(prediction, "Unknown")
