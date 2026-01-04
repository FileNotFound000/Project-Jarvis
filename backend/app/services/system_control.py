import pyautogui
import os
import platform
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class SystemControlService:
    def __init__(self):
        # Fail-safe: moving mouse to corner will throw exception
        pyautogui.FAILSAFE = True
        self.system = platform.system()

    def set_volume(self, level: int):
        """
        Set system volume to a specific level (0-100).
        """
        try:
            if self.system == "Windows":
                devices = AudioUtilities.GetSpeakers()
                # interface = devices.Activate(
                #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                # volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume = devices.EndpointVolume
                
                # Volume range is usually -65.25 to 0.0
                # We need to map 0-100 to scalar 0.0-1.0
                scalar_volume = max(0.0, min(1.0, level / 100.0))
                volume.SetMasterVolumeLevelScalar(scalar_volume, None)
                return f"Volume set to {level}%"
            else:
                return "Volume control only supported on Windows for now."
        except Exception as e:
            print(f"Error setting volume: {e}")
            return f"Error setting volume: {str(e)}"

    def set_mute(self, mute: bool):
        """
        Set mute state (True for mute, False for unmute).
        """
        try:
            if self.system == "Windows":
                devices = AudioUtilities.GetSpeakers()
                volume = devices.EndpointVolume
                
                volume.SetMute(1 if mute else 0, None)
                return "Volume muted" if mute else "Volume unmuted"
            else:
                return "Mute control only supported on Windows for now."
        except Exception as e:
            print(f"Error setting mute: {e}")
            return f"Error setting mute: {str(e)}"

    def open_application(self, app_name: str):
        """
        Open an application.
        """
        try:
            if self.system == "Windows":
                # Simple startfile (works for registered apps and paths)
                # For common apps, we might need a mapping or just try the name
                os.startfile(app_name)
                return f"Opening {app_name}"
            else:
                return "App launching only supported on Windows for now."
        except Exception as e:
            # Try using pyautogui to press win key and type
            try:
                pyautogui.press('win')
                pyautogui.sleep(0.5)
                pyautogui.write(app_name)
                pyautogui.sleep(0.5)
                pyautogui.press('enter')
                return f"Attempting to open {app_name} via Start Menu"
            except Exception as e2:
                print(f"Error opening app: {e2}")
                return f"Error opening app: {str(e2)}"

    def take_screenshot(self):
        """
        Take a screenshot and return it.
        """
        try:
            screenshot = pyautogui.screenshot()
            return screenshot
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
