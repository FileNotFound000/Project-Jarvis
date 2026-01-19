import pyaudio
import vosk
import os
import sys

print("Testing Audio Environment...")

# Check VOSK Model
if not os.path.exists("model"):
    print("FAIL: 'model' directory not found.")
else:
    print("PASS: 'model' directory found.")
    try:
        model = vosk.Model("model")
        print("PASS: VOSK Model loaded successfully.")
    except Exception as e:
        print(f"FAIL: VOSK Model failed to load: {e}")

# Check PyAudio
try:
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    print(f"PyAudio detected {numdevices} devices on Host API 0.")
    
    found_input = False
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print(f"  - Input Device {i}: {p.get_device_info_by_host_api_device_index(0, i).get('name')}")
            found_input = True
            
    if not found_input:
        print("FAIL: No input devices (microphone) found!")
    else:
        print("PASS: Input devices found.")
        
    # Try opening stream
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    print("PASS: Stream opened successfully.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
except Exception as e:
    print(f"FAIL: PyAudio Error: {e}")

print("Test Complete.")
