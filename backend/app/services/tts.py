import edge_tts
import os
import uuid

AUDIO_DIR = "static/audio"

async def generate_audio(text: str, voice: str = "en-US-ChristopherNeural", session_id: str = None) -> str:
    """
    Generates audio from text and returns the filename (or relative path).
    """
    # Determine output directory
    output_dir = AUDIO_DIR
    if session_id:
        output_dir = os.path.join(AUDIO_DIR, session_id)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(output_dir, filename)
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)
    
    # Return path relative to static/audio if in subdirectory, else just filename
    # Actually, simpler is to just return relative path from static/audio root
    if session_id:
        return f"{session_id}/{filename}"
    return filename
