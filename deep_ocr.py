import torch
from craft import CRAFT
from crnn import CRNN

def load_craft_model(model_path):
    craft_model = CRAFT()
    craft_model.load_state_dict(torch.load(model_path))
    craft_model.eval()
    return craft_model

def load_crnn_model(model_path):
    crnn_model = CRNN()
    crnn_model.load_state_dict(torch.load(model_path))
    crnn_model.eval()
    return crnn_model

def deep_ocr(image, craft_model, crnn_model):
    # Implement the function that takes an image, uses the CRAFT model to detect text regions,
    # and then uses the CRNN model to recognize text in those regions
    pass
