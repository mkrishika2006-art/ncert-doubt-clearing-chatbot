import pyttsx3
import io

def generate_audio_from_text(text):
    """Generate audio from text and return bytes (MP3) instead of a file."""
    engine = pyttsx3.init()
    
    # Create an in-memory file
    audio_bytes = io.BytesIO()
    
    # Save speech to a temporary WAV file in memory
    temp_wav = "temp.wav"
    engine.save_to_file(text, temp_wav)
    engine.runAndWait()
    
    # Read WAV file bytes
    with open(temp_wav, "rb") as f:
        audio_bytes.write(f.read())
    
    audio_bytes.seek(0)
    return audio_bytes