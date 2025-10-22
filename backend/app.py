# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# from pymongo import MongoClient
# from datetime import datetime

# app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": "*"}})

# genai.configure(api_key="AIzaSyB4h-rGxAJjTfKgX7T-DbZsc8HnYqALEJA")
# model = genai.GenerativeModel("gemini-2.5-flash-lite")

# MONGO_URI = "mongodb+srv://priyachouhan23:priyachouhan23mongo@cluster0.1ce4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# client = MongoClient(MONGO_URI)
# db = client["text_summarizer_db"]      
# collection = db["summaries"]            

# @app.route('/summarize', methods=['POST'])
# def summarize_text():
#     data = request.get_json()
#     text = data.get("text", "").strip()

#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     try:
#         response = model.generate_content(f"Summarize the following text: {text}")
#         summary = response.text.strip()

#         record = {
#             "original_text": text,
#             "summary": summary,
#             "timestamp": datetime.utcnow()
#         }
#         collection.insert_one(record)

#         return jsonify({"summary": summary})
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/history', methods=['GET'])
# def get_history():
#     """Fetch all summaries stored in MongoDB"""
#     try:
#         data = list(collection.find({}, {"_id": 0}))  
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)



























from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# Get keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["text_summarizer_db"]
collection = db["summaries"]

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = model.generate_content(f"Summarize the following text: {text}")
        summary = response.text.strip()

        record = {
            "original_text": text,
            "summary": summary,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(record)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/history', methods=['GET'])
def get_history():
    """Fetch all summaries stored in MongoDB"""
    try:
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
