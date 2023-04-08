import torch
from craft import CRAFT
from crnn import CRNN

def load_craft_model(model_path):
    try:
        craft_model = CRAFT()
        craft_model.load_state_dict(torch.load(model_path))
        craft_model.eval()
    except FileNotFoundError:
        print(f"Error: Model file {model_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    return craft_model

def load_crnn_model(model_path):
    try:
        crnn_model = CRNN()
        crnn_model.load_state_dict(torch.load(model_path))
        crnn_model.eval()
    except FileNotFoundError:
        print(f"Error: Model file {model_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    return crnn_model

import cv2
import numpy as np

def deep_ocr(image, craft_model, crnn_model):
    # Convert PIL Image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Get text boxes and scores using CRAFT model
    boxes, _ = get_det_boxes(image, craft_model, text_threshold=0.7, link_threshold=0.4, low_text=0.4)
    boxes = adjust_result_coordinates(boxes, 1)
    
    # Initialize an empty string to store recognized text
    text = ""

    # For each text box, extract the text using CRNN model
    for box in boxes:
        x_min, y_min, x_max, y_max = box.astype(int)
        cropped_image = image[y_min:y_max, x_min:x_max]
        prediction = crnn_model(torch.tensor(cropped_image).unsqueeze(0))
        decoded_text = decode_predictions(prediction)
        text += decoded_text + "\n"

    return text
