from flask import Flask, request, jsonify
import os
import time
from datetime import datetime

app = Flask(__name__)

# Route to handle POST requests
@app.route('/file_age', methods=['POST'])
def file_age():
    
    # Retrieve file path from JSON payload sent with POST request
    data = request.json
    file_path = data['file_path']
    
    # Check if the file exists on the server
    if os.path.exists(file_path):
        # Last modification time
        modification_time = os.path.getmtime(file_path)
        modification_date = datetime.fromtimestamp(modification_time)
        # Current time
        current_time = datetime.now()
        # Calculate age
        age = current_time - modification_date
        return jsonify({"file_age": str(age), "status": "success"})
    else:
        return jsonify({"error": "File does not exist", "status": "fail"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
