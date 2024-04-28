from flask import Flask, request, jsonify, make_response
import requests
import json

# import os
# import sys

# root_directory = os.path.dirname(os.path.abspath(__file__))
# src_directory = os.path.join(root_directory, 'src')
# sys.path.insert(0, src_directory)

from src.augmented_generation import AugmentedGeneration

app = Flask(__name__)

################### QUESTIONS ###################
# DEFINE RAG MODEL -> questions

def load_RAG():
    return AugmentedGeneration()

@app.route('/api/questions', methods=['POST'])
def handle_questions():
    try:
        # Get the JSON data from the request
        data = request.json
        questions = data.get('questions', [])
        # Initialize a list to store the answers
        all_answers = []

        headers = {"Content-Type": "application/json"}

        for question in questions:

            question_text = question.get('question', '')

            answer, sources, topic = RAG_model.generate_answer(query = question_text)

            all_answers.append({
            "id": question.get('id', ''),
            "question": question_text,
            "topic": topic,
            "answer": answer
            })

        print(f"Questions: {questions}")

        # Construct the final response JSON
        response_json = {"questions": all_answers}

        # Create the HTTP response with the appropriate headers
        http_response = make_response(jsonify(response_json))
        http_response.headers['Content-Type'] = 'application/json'
        # Return the HTTP response
        return http_response, 200
    except Exception as e:
        # If an error occurs, return an error response with status code 400
        return jsonify({'error': str(e)}), 400


################### CONVERSATION ###################

@app.route('/api/converse', methods=['POST'])
def handle_conversation():
    try:
        # Get the JSON data from the request
        data = request.json
        questions = data.get('questions', [])

        # Initialize a list to store the answers
        all_answers = []

        # Perform subsequent requests for each question
        generate_url = 'http://10.10.6.10:8083/generate'
        headers = {"Content-Type": "application/json"}

        for question in questions:
            context = "You are a medical assistant who gives precise and short answers to medical queries.\n\n "
            question_raw = question.get('question', '')
            question_text = context + question_raw
            print(f"Question raw: {question_raw}")
            print(f"Question text: {question_text}")
            # Send a request for the current question
            data = {"inputs": question_text}
            response = requests.post(generate_url, json=data, headers=headers)

            # Get the answer for the current question (using the response content directly)
            answer_json = json.loads(response.text)
            generated_text = answer_json.get("generated_text", "")

            # Add the question, answer, and other metadata to the list of all answers
            all_answers.append({
                "id": question.get('id', ''),
                "question": question_raw,
                "topic": question.get('topic', ''),
                "answer": generated_text.strip()  # Remove leading/trailing whitespace
            })

        # Construct the final response JSON
        response_json = {"questions": all_answers}

        # Create the HTTP response with the appropriate headers
        http_response = make_response(jsonify(response_json))
        http_response.headers['Content-Type'] = 'application/json'

        # Return the HTTP response
        return http_response, 200
    except Exception as e:
        # If an error occurs, return an error response with status code 400
        return jsonify({'error': str(e)}), 400

################### PHOTOS ###################


# # DEFINE RESNET -> photos
# def load_Resnet():
#     return None

# RES_PATH = "../res"
# MODELS_PATH = os.path.join(RES_PATH, "models")
# RESNET_MODEL_PATH = os.path.join(MODELS_PATH, os.path.join("resnet", "model.pkl"))
# learn = load_learner(RESNET_MODEL_PATH)

# @app.route('/api/photo', methods=['POST'])
# def handle_photo():
#     if img in request.files:
#         img = request.files["image"]
#         img_resized = img.resize((224, 224), Image.BILINEAR)
#         pred_class, pred_idx, outputs = learn.predict(img)


#     return None

################### MAIN ###################

# Initialize models when the Flask application starts
if __name__ == '__main__':
    print("Initializing models...")
    try:
        RAG_model = load_RAG()
        resnet_model = load_Resnet()
        print("Models initialized successfully.")
    except Exception as e: 
        print("Error initializing models:", str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



# Now, your Flask app should be running and accessible to other computers on the same network.
# Other devices can make requests to your Flask app using your computer's IP address and the port you specified (e.g., http://your_computer_ip:8080/api/questions).
# Make sure your computer's firewall settings allow incoming connections on the specified port.