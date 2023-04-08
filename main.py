import os
import pdf_utils
import opennmt
import deep_ocr

def main():
    # Paths to input and output PDF files
    pdf_path = "path/to/your/pdf"
    output_path = "path/to/your/output_pdf"

    # Load the trained translation model, CRAFT model, and CRNN model
    try:
        model = opennmt.load_model("path/to/your/trained/model")
        craft_model = deep_ocr.load_craft_model("path/to/your/craft/model")
        crnn_model = deep_ocr.load_crnn_model("path/to/your/crnn/model")
    except FileNotFoundError:
        print("Error: Trained model, CRAFT, or CRNN model file not found.")
        return

    # Convert the PDF file to a list of preprocessed images and extract layout information
    try:
        images = pdf_utils.pdf_to_images(pdf_path)
        layout_data = pdf_utils.extract_layout(pdf_path)
    except FileNotFoundError:
        print(f"Error: Input PDF file {pdf_path} not found.")
        return

    # Extract text from each image and translate it using the pre-trained model
    translated_texts = []
    for image in images:
        preprocessed_image = pdf_utils.preprocess_image(image)
        text = pdf_utils.image_to_text(preprocessed_image, craft_model, crnn_model)
        translated_text = pdf_utils.translate_text(text, model)
        translated_texts.append(translated_text)

    # Generate a new PDF with the translated text in the same format as the original PDF
    pdf_utils.create_translated_pdf(layout_data, translated_texts, output_path)

if __name__ == "__main__":
    main()
