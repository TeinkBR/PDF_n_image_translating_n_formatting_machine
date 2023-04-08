import argparse
import json
import os
import pdf_utils
import opennmt
import deep_ocr

def main():
    # Parse command-line arguments or load from configuration file
    parser = argparse.ArgumentParser(description="Translate PDF documents using OCR and deep learning.")
    parser.add_argument("--input", type=str, required=False, help="Input PDF file path.")
    parser.add_argument("--output", type=str, required=False, help="Output translated PDF file path.")
    parser.add_argument("--model", type=str, required=False, help="Path to the deep learning model.")
    args = parser.parse_args()

    if args.input and args.output and args.model:
        input_pdf_path = args.input
        output_pdf_path = args.output
        model_path = args.model
    else:
        with open("config.json", "r") as f:
            config = json.load(f)
        input_pdf_path = config["input_pdf_path"]
        output_pdf_path = config["output_pdf_path"]
        model_path = config["model_path"]

    # Load the trained translation model, CRAFT model, and CRNN model
    try:
        model = opennmt.load_model(model_path)
        craft_model = deep_ocr.load_craft_model(config["craft_model_path"])
        crnn_model = deep_ocr.load_crnn_model(config["crnn_model_path"])
    except FileNotFoundError:
        print("Error: Trained model, CRAFT, or CRNN model file not found.")
        return

    # Convert the PDF file to a list of preprocessed images and extract layout information
    try:
        images = pdf_utils.pdf_to_images(input_pdf_path)
        layout_data = pdf_utils.extract_layout(input_pdf_path)
    except FileNotFoundError:
        print(f"Error: Input PDF file {input_pdf_path} not found.")
        return

    # Extract text from each image and translate it using the pre-trained model
    translated_texts = []
    for image in images:
        preprocessed_image = pdf_utils.preprocess_image(image)
        text = pdf_utils.image_to_text(preprocessed_image, craft_model, crnn_model)
        translated_text = pdf_utils.translate_text(text, model)
        translated_texts.append(translated_text)

    # Generate a new PDF with the translated text in the same format as the original PDF
    pdf_utils.create_translated_pdf(layout_data, translated_texts, output_pdf_path)

if __name__ == "__main__":
    main()
