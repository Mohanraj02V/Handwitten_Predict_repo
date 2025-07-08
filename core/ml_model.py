import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import os
from django.conf import settings

# Define CNN Model (same as your original)
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 28 → 14
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 14 → 7
            nn.Flatten(),
            nn.Linear(7 * 7 * 64, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        return self.net(x)

# Load the model
def load_model():
    model = CNNModel()
    model_path = os.path.join(settings.BASE_DIR, 'best_model.pth')
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

# Preprocess image
def preprocess_image(image):
    # Convert to grayscale if not already
    img = image.convert('L')
    
    # Invert if needed (white digits on black background)
    if np.array(img).mean() > 127:  # if background is light
        img = ImageOps.invert(img)
    
    # Add some blur and thresholding to thicken thin lines
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img = img.point(lambda x: 0 if x < 30 else 255)  # threshold
    
    # Resize to 28x28 with antialiasing
    img = img.resize((28, 28), Image.LANCZOS)
    
    # Convert to tensor and normalize like MNIST
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    img_tensor = transform(img).unsqueeze(0)
    return img_tensor

# Make prediction
def predict_digit(image):
    model = load_model()
    with torch.no_grad():  # This line starts a context manager
        img_tensor = preprocess_image(image)  # Must be indented
        output = model(img_tensor)            # Must be indented
        _, predicted = torch.max(output, 1)  # Must be indented
        return predicted.item()