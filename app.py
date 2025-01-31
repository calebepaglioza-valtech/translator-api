from flask import Flask, request, jsonify
import openai
import os

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# API route for translating Swedish text to English
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    swedish_text = data.get("swedish_text", "")

    if not swedish_text:
        return jsonify({"error": "No text provided"}), 400

    # Use GPT-4o-mini to translate Swedish to English
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate Swedish to English."},
            {"role": "user", "content": swedish_text}
        ]
    )

    english_translation = response.choices[0].message.content  # New syntax

    return jsonify({"english_translation": english_translation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Run in debug mode for error tracking