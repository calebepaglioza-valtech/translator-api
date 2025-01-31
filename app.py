from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    return "Translator API is running with audio support!"

# 🟢 Existing text translation function
@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    swedish_text = data.get("swedish_text", "")

    if not swedish_text:
        return jsonify({"error": "No text provided"}), 400

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate Swedish to English."},
            {"role": "user", "content": swedish_text}
        ]
    )

    return jsonify({"english_translation": response.choices[0].message.content})

# 🔵 New function to handle live audio translation
@app.route('/translate-audio', methods=['POST'])
def translate_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    
    # Convert speech to text using Whisper API
    transcript_response = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    
    swedish_text = transcript_response.text

    # Translate the transcribed text to English
    translation_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate Swedish to English."},
            {"role": "user", "content": swedish_text}
        ]
    )

    return jsonify({
        "transcribed_text": swedish_text,
        "english_translation": translation_response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)