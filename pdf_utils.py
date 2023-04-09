import cv2
import pytesseract
from PIL import Image
import numpy as np
from pdf2image import convert_from_path
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal
import opennmt

def pdf_to_images(pdf_path, dpi):
    return convert_from_path(pdf_path, dpi)

def preprocess_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def image_to_text(image, _craft_model=None, _crnn_model=None):
    img = Image.fromarray(image)
    text = pytesseract.image_to_string(img, lang='eng')
    return text

def extract_layout(pdf_path):
    layout_data = []
    for page_layout in extract_pages(pdf_path):
        layout_page = []
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                layout_page.append(element)
        layout_data.append(layout_page)
    return layout_data

def translate_texts(texts, model, target_language, beam_width, length_penalty):
    translations = []
    for text in texts:
        translation = opennmt.translate(text, model, target_language, beam_width, length_penalty)
        translations.append(translation)
    return translations
