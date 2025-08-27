from io import BytesIO
from openai import OpenAI
from Testing.Module.ConnectOpenAI import connect_openai_api # For connecting to api
from Testing.Module.SendMessageToOpenAI import send_receive_message # For communicate with model
import base64
import mss
from PIL import Image

def capture_screen():
    """
    Capture the current screen and return the img
    :return: image (type:Unknown)
    """
    with mss.mss() as s:
        # Capture the screen
        screenshot = s.grab(s.monitors[1]) # Capture the first monitor

        # Convert to PIL Image
        return Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')

def encode_image(image):
    """
    Read in the image to the buffer, and encoding it to base64 format
    :param image: image (type:Unknown)
    :return: base64 image (type:Unknown)
    """
    with BytesIO() as buffer:
        # Use a buffer to save the image
        image.save(buffer, format='PNG')
        buffer.seek(0) # Move to the beginning of the BytesIO buffer
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def main(prompt):
    """
    The main function for the whole pipline
    :return: None
    """
    client = connect_openai_api()
    screenshot = capture_screen()

    b64_img = encode_image(screenshot)

    try:
        response = send_receive_message(client, prompt, b64_img).output_text
        return response
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main(input("Hello"))