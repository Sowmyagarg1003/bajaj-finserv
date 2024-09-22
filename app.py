import base64

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins (you can restrict this later)

def process_file(file_b64):
    if not file_b64:
        return {
            "file_valid": False,
            "file_mime_type": None, 
            "file_size_kb": 0
        }
    try:
        file_data = base64.b64decode(file_b64)
        file_size_kb = len(file_data) / 1024  
        file_mime_type = "image/png"  # This should be determined based on the file content
        
        return {
            "file_valid": True,
            "file_mime_type": file_mime_type,
            "file_size_kb": round(file_size_kb, 2)
        }
    except Exception as e:
        print(f"File processing error: {e}")  # Log file processing error
        return {
            "file_valid": False,
            "file_mime_type": None,
            "file_size_kb": 0
        }

# POST method
@app.route('/bfhl', methods=['POST'])
def process_data():
    print("process_data endpoint hit")  # Log that the endpoint was called
    try:
        if request.json is None:
            return jsonify({"is_success": False, "error": "No JSON data provided"}), 400
        
        print("Request JSON:", request.json)  # Log the incoming JSON
        data = request.json.get('data', [])
        file_b64 = request.json.get('file_b64', None)

        # Validate file_b64
        if file_b64 is not None and not isinstance(file_b64, str):
            return jsonify({"is_success": False, "error": "Invalid base64 string"}), 400

        user_id = "Sowmya_Garg_10032004" 
        email = "ss3310@srmist.edu.in"
        roll_number = "RA2111003030017"

        # Filter numbers and alphabets from the data
        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha()]
        lowercase_alphabets = [item for item in alphabets if item.islower()]

        # Get the highest lowercase alphabet
        highest_alphabet = max(lowercase_alphabets) if lowercase_alphabets else None

        # Process the file if provided
        file_info = process_file(file_b64)

        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": [highest_alphabet] if highest_alphabet else [],
            **file_info
        }

        print("Response:", response)  # Log the constructed response
        return jsonify(response), 200

    except Exception as e:
        print(f"Error: {e}")  # Log error details
        return jsonify({"is_success": False, "error": str(e)}), 400

@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    return jsonify({"operation_code": 1}), 200

if __name__ == '__main__':
    app.run(debug=True)
