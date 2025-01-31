import openai
import pyaudio
import wave
import soundfile as sf
import yt_dlp
import os
import time

# Set your OpenAI API key
openai.api_key = "your_openai_api_key_here"  # Replace with your API key

# Function to record live audio from the microphone
def record_audio(filename="input.wav", duration=5, sample_rate=16000):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)

    frames = []
    print("Recording...")

    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    return filename

# Function to transcribe Swedish audio using Whisper
def transcribe_audio(filename="input.wav"):
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

# Function to translate Swedish text to English
def translate_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Translate Swedish to English accurately."},
                  {"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]

# Function to generate English audio from text
def text_to_speech(text, output_filename="output.wav"):
    response = openai.Audio.create(
        model="tts-1",
        input=text,
        voice="alloy"  # Available voices: alloy, echo, fable, onyx, nova, shimmer
    )
    with open(output_filename, "wb") as f:
        f.write(response["audio"])
    return output_filename

# Function to extract audio from YouTube videos
def extract_audio_from_youtube(video_url, output_filename="youtube_audio.wav"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return output_filename

# Function to run the live translation process
def live_translate():
    while True:
        audio_file = record_audio(duration=5)  # Capture 5 seconds of live audio
        swedish_text = transcribe_audio(audio_file)  # Transcribe
        english_translation = translate_text(swedish_text)  # Translate
        audio_output = text_to_speech(english_translation)  # Generate English speech

        print(f"Swedish: {swedish_text}")
        print(f"English: {english_translation}")

        os.system(f"afplay {audio_output}")  # Play the translated audio (Mac only)
        time.sleep(1)  # Small delay before the next iteration

# Run the live translation
if __name__ == "__main__":
    print("Starting Live Swedish-to-English Translation...")
    live_translate()