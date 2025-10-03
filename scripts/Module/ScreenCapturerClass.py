from io import BytesIO
from openai import OpenAI
from PIL import Image
import base64, mss

class ScreenCapturer:
    def __init__(self, encode_type=None):
        self.encode_type = encode_type
        self.image = None

    def capture_screen(self):
        """
        Capture the current screen and return the img
        :return: None
        """
        with mss.mss() as s:
            # Capture the screen
            screenshot = s.grab(s.monitors[1]) # Capture the first monitor

            # Convert to PIL Image
            self.image = Image.frombytes(
                'RGB',
                screenshot.size,
                screenshot.bgra,
                'raw',
                'BGRX'
            )
    # TODO: Try original image instead of base64
    def encode_image(self):
        """
        Read in the image to the buffer, and encoding it to base64 format
        :return: None
        """
        with BytesIO() as buffer:
            # Use a buffer to save the image
            self.image.save(buffer, format='PNG')
            buffer.seek(0) # Move to the beginning of the BytesIO buffer
            self.image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    def get_screenshot(self):
        """
        The main function for the whole pipline
        :return: response (type:string-like)
        """
        self.capture_screen()
        self.encode_image()

    def get_image(self):
        return self.image

if __name__ == "__main__":
    pass