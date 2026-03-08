from gtts import gTTS

def generate_audio_from_text(text):
    output_file = "output_audio.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)
    return output_file
