import argparse
import json
import logging
import os
import pdf_utils
import deep_ocr
import opennmt
from multiprocessing import Pool

def process_image(image):
    preprocessed_image = pdf_utils.preprocess_image(image)
    text = pdf_utils.image_to_text(preprocessed_image, craft_model, crnn_model)
    return text

def main():
    # Setup logging
    logging.basicConfig(filename='pdf_translator.log', level=logging.DEBUG)

    # Parse command-line arguments or load from config file
    parser = argparse.ArgumentParser(description="Translate PDF documents using OCR and deep learning.")
    parser.add_argument("--input", type=str, required=True, help="Input PDF file path.")
    parser.add_argument("--output", type=str, required=True, help="Output translated PDF file path.")
    parser.add_argument("--model", type=str, required=True, help="Path to the deep learning model.")
    parser.add_argument("--craft-model", type=str, required=True, help="Path to the CRAFT model.")
    parser.add_argument("--crnn-model", type=str, required=True, help="Path to the CRNN model.")
    parser.add_argument("--dpi", type=int, default=300, help="DPI of the output images.")
    args = parser.parse_args()

    # Load the trained translation model, CRAFT model, and CRNN model
    try:
        model = opennmt.load_model(args.model)
        craft_model = deep_ocr.load_craft_model(args.craft_model)
        crnn_model = deep_ocr.load_crnn_model(args.crnn_model)
    except FileNotFoundError:
        logging.error("Trained model, CRAFT, or CRNN model file not found.")
        return

    # Convert the PDF file to a list of preprocessed images and extract layout information
    try:
        images = pdf_utils.pdf_to_images(args.input, args.dpi)
        layout_data = pdf_utils.extract_layout(args.input)
    except FileNotFoundError:
        logging.error(f"Input PDF file {args.input} not found.")
        return

    # Extract text from each image using OCR in parallel
    with Pool() as pool:
        texts = pool.map(process_image, images)

    # Translate the extracted texts using the pre-trained model
    try:
        translated_texts = pdf_utils.translate_texts(texts, model)
    except Exception as e:
        logging.error(f"Error: {e}")
        return

    # Generate a new PDF with the translated text in the same format as the original PDF
    try:
        pdf_utils.create_translated_pdf(layout_data, translated_texts, args.output)
    except Exception as e:
        logging.error(f"Error: {e}")
        return

if __name__ == "__main__":
    main()
