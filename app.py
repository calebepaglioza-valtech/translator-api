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
        print("❌ No audio file uploaded!")
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    print(f"✅ Received Audio File: {audio_file.filename}")

    try:
        # Convert the FileStorage object to bytes
        audio_bytes = audio_file.read()  

        # Convert speech to text using Whisper API
        print("🔄 Sending file to Whisper API...")
        transcript_response = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", audio_bytes, "audio/wav")  # Convert to proper format
        )

        swedish_text = transcript_response.text
        print(f"✅ Transcribed Text: {swedish_text}")

        # Translate text to English
        print("🔄 Sending text to GPT-4o-mini for translation...")
        translation_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate Swedish to English."},
                {"role": "user", "content": swedish_text}
            ]
        )

        english_translation = translation_response.choices[0].message.content
        print(f"✅ Translated Text: {english_translation}")

        return jsonify({
            "transcribed_text": swedish_text,
            "english_translation": english_translation
        })

    except Exception as e:
        print(f"❌ API Error: {e}")  # Logs the error in the server logs
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)