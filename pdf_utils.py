from pdf2image import convert_from_path
from PIL import Image
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from reportlab.pdfgen import canvas

import deep_ocr
import os


def create_translated_pdf(layout_data, translated_texts, output_path):
    """Generates a new PDF with the translated text in the same format as the original PDF using reportlab."""
    c = canvas.Canvas(output_path)

    # Use layout_data to position and format the translated text
    for i, layout in enumerate(layout_data):
        for textbox in layout:
            if isinstance(textbox, LTTextBox):
                x, y, w, h = textbox.bbox
                font_size = textbox.get_text().split('\n')[0].size
                font_name = textbox.get_text().split('\n')[0].fontname
                c.setFont(font_name, font_size)
                # Draw the translated text in the same position as the original text
                c.drawString(x, y, translated_texts[i])

    c.save()


def preprocess_image(image):
    """Preprocesses a PIL Image object for OCR."""
    # Convert the image to grayscale
    image = image.convert('L')
    # Resize the image to a smaller size (e.g., 800x800)
    image = image.resize((800, 800))
    # Apply other preprocessing steps here, e.g., thresholding, denoising, etc.
    return image


def image_to_text(image, craft_model, crnn_model):
    """Extracts text from a PIL Image object using deep learning OCR."""
    text = deep_ocr.deep_ocr(image, craft_model, crnn_model)
    return text


def extract_layout(pdf_path):
    """Extracts layout information (position, font size, etc.) from a PDF file using pdfminer."""
    resource_manager = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)

    layout_data = []

    try:
        with open(pdf_path, "rb") as f:
            for page in PDFPage.get_pages(f):
                interpreter.process_page(page)
                layout = device.get_result()
                layout_data.append(layout)
    except FileNotFoundError:
        print(f"Error: File {pdf_path} not found.")
        return []

    return layout_data


def pdf_to_images(pdf_path):
    """Converts a PDF file to a list of PIL Image objects."""
    try:
        images = convert_from_path(pdf_path)
    except FileNotFoundError:
        print(f"Error: File {pdf_path} not found.")
        return []

    return images
