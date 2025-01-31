import requests
import pyaudio
import wave

API_URL = "https://translator-api-thy8.onrender.com/translate-audio"

def record_audio(filename="audio.wav", duration=5, sample_rate=16000):
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

def send_audio():
    audio_file = record_audio()
    print(f"Sending {audio_file} to API...")
    
    response = requests.post(
        API_URL,
        files={"audio": open(audio_file, "rb")}
    )

    print("Response:", response.json())

if __name__ == "__main__":
    send_audio()