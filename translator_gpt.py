import openai
import requests

openai_client = openai.OpenAI(api_key="OPENAI_API_KEY")

def translate_swedish_to_english(text):
    """ Calls the Translator API to translate Swedish text to English """
    response = requests.post(
        "https://translator-api-thy8.onrender.com/translate",
        json={"swedish_text": text},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        return response.json().get("english_translation", "Translation failed")
    else:
        return "Error in API request"

# Example: Use OpenAI GPT with Function Calling
response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Translate Swedish text to English using an external API."},
        {"role": "user", "content": "Hej, hur mår du?"}
    ],
    functions=[
        {
            "name": "translate_swedish_to_english",
            "description": "Translate Swedish text to English",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Swedish text to be translated"}
                },
                "required": ["text"]
            }
        }
    ],
    function_call={"name": "translate_swedish_to_english"}
)

# Extract function arguments and call API
function_args = response.choices[0].message.function_call.arguments
translation = translate_swedish_to_english(function_args["text"])

print("English Translation:", translation)