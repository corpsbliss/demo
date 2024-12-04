import pytesseract
from PIL import Image

# Install and configure Tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Take screenshot with Selenium
driver.save_screenshot("screenshot.png")

# Extract text from image
text = pytesseract.image_to_string(Image.open("screenshot.png"))

# Check if expected text appears
if "Expected App Title" in text:
    print("App launched successfully!")
else:
    print("Text not found, UI might have changed!")