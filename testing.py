import os
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import json

# Load the trained model
model = load_model("item_classifier.h5")

# Load class indices from the JSON file
with open('class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)

# Invert the dictionary to map indices back to class names
class_labels = {v: k for k, v in class_indices.items()}

# Define the path to the testing directory
test_dir = 'images/Testing'

# Get all image file paths in the testing directory
test_images = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if f.endswith(('png', 'jpg', 'jpeg'))]

# Function to preprocess and predict the class of a single image
def predict_image(image_path, model):
    # Read the image
    img = cv2.imread(image_path)

    # Resize the image to the model's expected input size (128x128)
    img_resized = cv2.resize(img, (128, 128))

    # Convert the image from BGR (OpenCV format) to RGB
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

    # Normalize the image (same as during training)
    img_normalized = img_rgb / 255.0

    # Expand dimensions to match the input shape (1, 128, 128, 3)
    img_input = np.expand_dims(img_normalized, axis=0)

    # Make a prediction using the model
    predictions = model.predict(img_input)

    # Get the predicted class index and its corresponding probability
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_prob = predictions[0][predicted_class_index]

    # Get the class name from the predicted index
    predicted_class_name = class_labels[predicted_class_index]

    return predicted_class_name, predicted_prob

# Iterate over the test images and print the predictions
for image_path in test_images:
    predicted_class_name, predicted_prob = predict_image(image_path, model)
    print(f"Image: {os.path.basename(image_path)}")
    print(f"Predicted Class: {predicted_class_name}, Probability: {predicted_prob:.4f}\n")

print("Testing completed.")
