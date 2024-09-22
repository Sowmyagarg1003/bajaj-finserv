import base64

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://bajaj-finserv-frontend-rhie83wn9-sowmya-gargs-projects.vercel.app'])

def process_file(file_b64):
    try:
        file_data = base64.b64decode(file_b64)
        file_size_kb = len(file_data) / 1024  

     
        file_mime_type = "image/png"
        
        return {
            "file_valid": True,
            "file_mime_type": file_mime_type,
            "file_size_kb": round(file_size_kb, 2)
        }
    except Exception as e:
        return {
            "file_valid": False,
            "file_mime_type": None,
            "file_size_kb": 0
        }

# POST method
@app.route('/bfhl', methods=['POST'])
def process_data():
    try:
        data = request.json.get('data', [])
        file_b64 = request.json.get('file_b64', None)

        user_id = "Sowmya_Garg_10032004" 
        email = "ss3310@srmist.edu.in"
        roll_number = "RA2111003030017"

        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha()]
        lowercase_alphabets = [item for item in alphabets if item.islower()]
        
        print("Lowercase Alphabets:", lowercase_alphabets)
        highest_alphabet = max(lowercase_alphabets) if lowercase_alphabets else "No lowercase alphabet found"



        if file_b64:
            file_info = process_file(file_b64)
        else:
            file_info = {
                "file_valid": False,
                "file_mime_type": None,
                "file_size_kb": 0
            }

        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": highest_alphabet,
            **file_info 
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 400

@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    return jsonify({"operation_code": 1}), 200

if __name__ == '__main__':
    app.run(debug=True)
