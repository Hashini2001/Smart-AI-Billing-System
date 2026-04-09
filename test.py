import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json

# Load the trained model
model = tf.keras.models.load_model('item_classifier.h5')

# Load class indices from JSON file
with open('class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)
    class_names = list(class_indices.keys())
    print("Class names:", class_names)

# Function to preprocess the image for the model
def preprocess_image(img):
    img = cv2.resize(img, (128, 128))  # Resize image to match model's input shape
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Wait for the user to press 'c' to capture an image
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):  # 'c' key to capture the image
        # Preprocess the image
        img = preprocess_image(frame)
        
        # Make a prediction
        predictions = model.predict(img)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        predicted_class_name = class_names[predicted_class_index]
        predicted_probability = predictions[0][predicted_class_index]

        # Display the prediction
        print(f"Predicted Class: {predicted_class_name}, Probability: {predicted_probability:.4f}")

    elif key == ord('q'):  # 'q' key to quit
        print("Exiting...")
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
