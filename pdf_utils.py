from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def pdf_to_images(pdf_path):
    """Converts a PDF file to a list of PIL Image objects."""
    return convert_from_path(pdf_path)


def preprocess_image(image):
    """Preprocesses a PIL Image object for OCR."""
    # Convert the image to grayscale
    image = image.convert('L')
    # Resize the image to a smaller size (e.g., 800x800)
    image = image.resize((800, 800))
    # Apply other preprocessing steps here, e.g., thresholding, denoising, etc.
    return image


def image_to_text(image):
    """Extracts text from a PIL Image object using OCR."""
    text = pytesseract.image_to_string(image)
    return text


def extract_layout(pdf_path):
    """Extracts layout information (position, font size, etc.) from a PDF file using pdfminer."""
    resource_manager = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)

    layout_data = []

    with open(pdf_path, "rb") as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
            layout = device.get_result()
            # Extract layout information (position, font size, etc.) and store it in layout_data
            layout_data.append(layout)

    return layout_data
