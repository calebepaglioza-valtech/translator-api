from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

OPENAI_API_KEY = "OPENAI_API_KEY"

@app.route("/chat", methods=["POST"])
def chat_with_gpt():
    user_input = request.json.get("message", "")

    # Detect if translation is needed
    if "translate:" in user_input.lower():
        swedish_text = user_input.split("translate:")[1].strip()
        response = requests.post(
            "https://translator-api-thy8.onrender.com/translate",
            json={"swedish_text": swedish_text},
            headers={"Content-Type": "application/json"}
        )
        return jsonify({"response": response.json().get("english_translation", "Translation failed")})

    # Otherwise, use OpenAI GPT for normal conversation
    openai_response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        api_key=OPENAI_API_KEY
    )

    return jsonify({"response": openai_response["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)