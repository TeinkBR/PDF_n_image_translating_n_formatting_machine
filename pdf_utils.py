from pdf2image import convert_from_path
from PIL import Image


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
