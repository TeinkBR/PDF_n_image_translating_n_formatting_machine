import torch
import numpy as np
import cv2
from craft import CRAFT
from crnn import CRNN
from utils import get_det_boxes, adjust_result_coordinates, decode_predictions


def load_craft_model(model_path):
    """Loads a pre-trained CRAFT model from a file."""
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found.")
    try:
        with torch.no_grad():
            craft_model = CRAFT()
            craft_model.load_state_dict(torch.load(model_path))
            craft_model.eval()
    except Exception as e:
        raise Exception(f"Error while loading CRAFT model: {str(e)}")
    return craft_model


def load_crnn_model(model_path):
    """Loads a pre-trained CRNN model from a file."""
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found.")
    try:
        with torch.no_grad():
            crnn_model = CRNN()
            crnn_model.load_state_dict(torch.load(model_path))
            crnn_model.eval()
    except Exception as e:
        raise Exception(f"Error while loading CRNN model: {str(e)}")
    return crnn_model


def deep_ocr(image, craft_model, crnn_model, text_threshold=0.7, link_threshold=0.4, low_text=0.4):
    """
    Extracts text from an input image using deep learning OCR.

    Parameters:
    image (PIL.Image): The input image.
    craft_model (CRAFT): The CRAFT model for text detection.
    crnn_model (CRNN): The CRNN model for text recognition.
    text_threshold (float): The threshold value for text detection by the CRAFT model.
    link_threshold (float): The threshold value for link detection by the CRAFT model.
    low_text (float): The threshold value for discarding text regions with low confidence.

    Returns:
    str: The recognized text.
    """
    # Convert PIL Image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Get text boxes and scores using CRAFT model
    boxes, _ = get_det_boxes(image, craft_model, text_threshold=text_threshold, link_threshold=link_threshold, low_text=low_text)
    boxes = adjust_result_coordinates(boxes, 1)

    # Initialize an empty string to store recognized text
    text = ""

    # For each text box, extract the text using CRNN model
    for box in boxes:
        x_min, y_min, x_max, y_max = box.astype(int)
        if x_max - x_min < 10 or y_max - y_min < 10:
            continue
        cropped_image = image[y_min:y_max, x_min:x_max]

        # Convert the cropped image to grayscale and resize it
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        cropped_image = cv2.resize(cropped_image, (100, 32))

        with torch.no_grad():
            prediction = crnn_model(torch.tensor(cropped_image).unsqueeze(0).unsqueeze(1))
        decoded_text = decode_predictions(prediction)
        text += decoded_text + "\n"

    # Handle case where no text is detected
    if text == "":
        text = "No text detected."

    return text
