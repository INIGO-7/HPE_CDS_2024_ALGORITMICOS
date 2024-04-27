from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

@app.route('/api/questions', methods=['POST'])
def process_questions():
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
            question_text = question.get('question', '')

            # Send a request for the current question
            data = {"inputs": question_text}
            response = requests.post(generate_url, json=data, headers=headers)

            # Get the answer for the current question (using the response content directly)
            answer_json = json.loads(response.text)
            generated_text = answer_json.get("generated_text", "")

            # Add the question, answer, and other metadata to the list of all answers
            all_answers.append({
                "id": question.get('id', ''),
                "question": question_text,
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

if __name__ == '__main__':
    app.run(debug=True)
