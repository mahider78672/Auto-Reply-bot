# Step 1: Imports
import pyautogui  
import pyperclip  
import time       
import openai     
from PIL import Image  
import pytesseract  

# Ensure you have Tesseract installed and its path set up
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set OpenAI API Key
openai.api_key = "your_openai_api_key"  # Replace with your API key

# Step 2: Open WhatsApp Web
def open_whatsapp_web():  
    print("Opening WhatsApp Web...")
    pyautogui.hotkey("ctrl", "t")  # Open new tab
    time.sleep(1)
    pyperclip.copy("https://web.whatsapp.com")  
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(5)  # Wait for WhatsApp Web to load

# Step 3: Select a Chat
def select_chat():  
    print("Selecting chat on WhatsApp Web...")
    chat_position = (310, 412)  # Adjust based on your WhatsApp Web layout
    time.sleep(1)
    pyautogui.click(chat_position)
    time.sleep(1)

# Step 4: Extract Chat Text Using OCR
def extract_chat_text_ocr():  
    print("Extracting chat text using OCR...")

    # Dynamically adjust screen size
    screen_width, screen_height = pyautogui.size()
    chat_window_coordinates = (screen_width // 4, screen_height // 5, screen_width // 2, screen_height // 2)
    
    screenshot = pyautogui.screenshot(region=chat_window_coordinates)
    
    screenshot.save("chat_screenshot.png")
    print("Screenshot saved as chat_screenshot.png")
    
    extracted_text = pytesseract.image_to_string(screenshot, lang="eng")
    
    print("Extracted Chat Text:")
    print(extracted_text)

    return extracted_text.strip()

# Step 5: Generate AI Response
def generate_response(user_message):
    print("Generating AI response...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_reply = response["choices"][0]["message"]["content"]
        print(f"AI Response: {ai_reply}")
        return ai_reply
    except Exception as e:
        print(f"Error in generating response: {e}")
        return "Sorry, I couldn't process your message."

# Step 6: Send Message in WhatsApp
def send_message(whatsapp_message):
    print("Sending message in WhatsApp...")
    pyperclip.copy(whatsapp_message)
    pyautogui.hotkey("ctrl", "v")  # Paste message
    time.sleep(1)
    pyautogui.press("enter")  # Press Enter to send

# Main Automation Flow
open_whatsapp_web()
select_chat()
message = extract_chat_text_ocr()

if message:
    response = generate_response(message)
    send_message(response)
else:
    print("No message detected.")