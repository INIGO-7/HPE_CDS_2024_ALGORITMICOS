from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
from fastai.vision.all import *
from fastai.learner import load_learner
import PIL
import os
from io import BytesIO
import base64


from src.augmented_generation import AugmentedGeneration

app = Flask(__name__)

# Spanish translations for wounds
wound_translations = {
    "Abrasions": "Abrasiones",
    "Bruises": "Moretones",
    "Burns": "Quemaduras",
    "Cut": "Cortes",
    "Diabetic Wounds": "Heridas diabéticas",
    "Laceration": "Laceraciones",
    "Normal": "Normal",
    "Pressure Wounds": "Heridas por presión",
    "Surgical Wounds": "Heridas quirúrgicas",
    "Venous Wounds": "Heridas venosas"
}

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
            context = "Eres un asistente médico que da respuestas concisas, precisas y completas a consultas médicas.\n\n "
            question_raw = question.get('question', '')
            question_text = context + question_raw
            print(f"Question raw: {question_raw}")
            print(f"Question text: {question_text}")
            # Send a request for the current question
            data = {"inputs": question_text,
                    "parameters":{"max_new_tokens":1500}
                    }
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

################### IMAGES ###################

# DEFINE RESNET -> images
def load_Resnet():
    return None

RES_PATH = "res"
MODELS_PATH = os.path.join(RES_PATH, "models")
RESNET_MODEL_PATH = os.path.join(MODELS_PATH, os.path.join("resnet", "resnet.pkl"))
learn = load_learner(RESNET_MODEL_PATH)

@app.route('/api/image', methods=['POST'])
def handle_image():
    try:
        if 'image' not in request.files:
            return "No image part", 400
        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400
        if file:
            # Convertir el objeto file en una imagen
            image = Image.open(file.stream)
            # Guardar la imagen en formato JPEG
            img_resized = image.resize((224, 224), Image.BILINEAR)  # Resize the image to match the input size expected by the model

            pred_class, pred_idx, outputs = learn.predict(img_resized)

            if pred_class != "Normal":
                answer, sources, topic = RAG_model.generate_answer(query = f"Eres un asistente médico, hispanohablante, que da respuestas concisas, precisas y completas a consultas médicas.\n\n He visto que tengo {wound_translations[pred_class].lower()} en mi piel. Rápido, qué hago?")
                print(answer)
                # Create the HTTP response with the appropriate headers
                response_json ={"response": f"{wound_translations[pred_class]}: {answer}"}
                http_response = make_response(jsonify(response_json))
                http_response.headers['Content-Type'] = 'application/json'
                # Return the HTTP response
                return http_response, 200
            else:
                generated_text = "No se pudo detectar ninguna anomalía en la foto que has enviado." 

                # Create the HTTP response with the appropriate headers
                http_response = make_response(jsonify(generated_text))
                http_response.headers['Content-Type'] = 'application/json'

                # Return the HTTP response
                return http_response, 200
    except Exception as e:
        # If an error occurs, return an error response with status code 400
        return jsonify({'error': str(e)}), 400


################### MAIN ###################

# Initialize models when the Flask application starts
if __name__ == '__main__':
    print("\n-----------------------------------------------------\nInitializing models...\n-----------------------------------------------------\n")
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