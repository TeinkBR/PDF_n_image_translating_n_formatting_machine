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
    parser.add_argument("--config", type=str, default="config.json", help="Path to the configuration file.")
    parser.add_argument("--input", type=str, help="Input PDF file path.")
    parser.add_argument("--output", type=str, help="Output translated PDF file path.")
    parser.add_argument("--model", type=str, help="Path to the deep learning model.")
    parser.add_argument("--craft-model", type=str, help="Path to the CRAFT model.")
    parser.add_argument("--crnn-model", type=str, help="Path to the CRNN model.")
    parser.add_argument("--dpi", type=int, help="DPI of the output images.")
    parser.add_argument("--target-language", type=str, help="Target language code for translation.")
    args = parser.parse_args()

    # Load settings from the configuration file
    with open(args.config, "r") as f:
        config = json.load(f)

    # Override configuration settings with command-line arguments, if provided
    input_pdf_path = args.input or config["input_pdf_path"]
    output_pdf_path = args.output or config["output_pdf_path"]
    model_path = args.model or config["model_path"]
    craft_model_path = args.craft_model or config["craft_model_path"]
    crnn_model_path = args.crnn_model or config["crnn_model_path"]
    dpi = args.dpi or config["dpi"]
    target_language = args.target_language or config["target_language"]

    # Load the trained translation model, CRAFT model, and CRNN model
    try:
        model = opennmt.load_model(model_path, target_language)
        craft_model = deep_ocr.load_craft_model(craft_model_path)
        crnn_model = deep_ocr.load_crnn_model(crnn_model_path)
    except FileNotFoundError:
        logging.error("Trained model, CRAFT, or CRNN model file not found.")
        return

    # Convert the PDF file to a list of preprocessed images and extract layout information
    try:
        images = pdf_utils.pdf_to_images(input_pdf_path, dpi)
        layout_data = pdf_utils.extract_layout(input_pdf_path)
    except FileNotFoundError:
        logging.error(f"Input PDF file {input_pdf_path} not found.")
        return

    # Extract text from each image using OCR in parallel
    with Pool() as pool:
        texts = pool.map(process_image, images)

    # Translate the extracted texts using the pre-trained model
    try:
        translated_texts = pdf_utils.translate_texts(texts, model, target_language)
    except Exception as e:
        logging.error(f"Error: {e}")
        return

    # Generate a new PDF with the translated text in the same format as the original PDF
    try:
        pdf_utils.create_translated_pdf(layout_data, translated_texts, output_pdf_path)
    except Exception as e:
        logging.error(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
