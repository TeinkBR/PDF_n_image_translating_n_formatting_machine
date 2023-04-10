import cv2
import pytesseract
import pandas as pd
import numpy as np

# Load handwritten image using OpenCV
img = cv2.imread('handwritten_note.png')

# Preprocess the image (convert to grayscale, threshold, blur)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
blur = cv2.medianBlur(thresh, 3)

# Perform OCR using Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(blur)

# Split the text into lines and remove empty lines
lines = [line.strip() for line in text.split('\n') if line.strip()]

# Split the lines into columns using whitespace as delimiter
data = [line.split() for line in lines]

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
df.to_csv('handwritten_note.csv', index=False, header=False)
