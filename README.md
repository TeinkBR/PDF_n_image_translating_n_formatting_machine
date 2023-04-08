# PDF_n_image_translating_n_formatting_machine

# PDF Translator
PDF Translator is a Python application that uses OCR and deep learning to translate PDF documents. It supports multiple languages and can output a translated PDF file in the same format as the original.

# Features
Convert a PDF file to a list of preprocessed images and extract layout information
Extract text from each image using OCR in parallel
Translate the extracted texts using a pre-trained deep learning model
Generate a new PDF with the translated text in the same format as the original PDF

# Installation

To install PDF Translator, run the following command:

>> pip install pdf_translator


# Usage
PDF Translator can be used from the command line or imported as a Python module.

# Command-line usage
To translate a PDF document, use the following command:
>> pdf_translator --input input.pdf --output output.pdf --model model.pt --craft-model craft.pt --crnn-model crnn.pt --dpi 300 --target-language fr

The options are as follows:

--input: Path to the input PDF file
--output: Path to the output translated PDF file
--model: Path to the pre-trained deep learning model
--craft-model: Path to the CRAFT model used for text detection
--crnn-model: Path to the CRNN model used for text recognition
--dpi: DPI of the output images (default is 300)
--target-language: Target language code for translation (e.g., fr for French)

