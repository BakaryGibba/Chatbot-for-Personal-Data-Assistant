import logging
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import worker  # Import the worker module

# Initialize Flask app and CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.logger.setLevel(logging.ERROR)

# Define the route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Render the index.html template

# Define the route for processing messages
@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json['userMessage']  # Extract the user's message from the request
    app.logger.info(f"Received user message: {user_message}")

    try:
        bot_response = worker.process_prompt(user_message)  # Process the user's message using the worker module
    except Exception as e:
        app.logger.error(f"Error processing user message: {e}")
        return jsonify({
            "botResponse": "There was an error processing your message. Please try again."
        }), 500

    # Return the bot's response as JSON
    return jsonify({
        "botResponse": bot_response
    }), 200

# Define the route for processing documents
@app.route('/process-document', methods=['POST'])
def process_document_route():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({
            "botResponse": "It seems like the file was not uploaded correctly, can you try again? If the problem persists, try using a different file."
        }), 400

    file = request.files['file']  # Extract the uploaded file from the request

    # Securely save the uploaded file to prevent path traversal attacks
    file_path = os.path.join("uploads", file.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)

    try:
        worker.process_document(file_path)  # Process the document using the worker module
    except Exception as e:
        app.logger.error(f"Error processing document: {e}")
        return jsonify({
            "botResponse": "There was an error processing the document. Please try again."
        }), 500

    # Return a success message as JSON
    return jsonify({
        "botResponse": "Thank you for providing your PDF document. I have analyzed it, so now you can ask me any questions regarding it!"
    }), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')
