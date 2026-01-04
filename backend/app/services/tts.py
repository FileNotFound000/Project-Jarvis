import edge_tts
import os
import uuid

AUDIO_DIR = "static/audio"

async def generate_audio(text: str, voice: str = "en-US-ChristopherNeural") -> str:
    """
    Generates audio from text and returns the filename.
    """
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)
    
    return filename
