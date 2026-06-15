from django.conf import settings
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load the trained model
def preprocess_image(image_path, img_size):
    image = load_img(image_path, target_size=(img_size, img_size))
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = image_array / 255.0
    return image_array, image

import cv2
import numpy as np

def check_color_threshold(image_path, min_valid_percentage=40):
    """
    Ensures the image contains a sufficient percentage of thermal-related colors.
    - Filters out non-thermal images based on HSV color filtering.
    - Ensures a minimum percentage of valid heat signature colors.
    """
    image = cv2.imread(image_path)
    if image is None:
        return False  # If the image can't be loaded, return False

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define thermal color ranges (Purple, Orange, Yellow, Red)
    lower_purple = np.array([120, 50, 50])
    upper_purple = np.array([160, 255, 255])

    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([30, 255, 255])

    lower_yellow = np.array([25, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create masks for each color
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Combine masks
    mask_combined = mask_purple | mask_orange | mask_yellow | mask_red

    # Calculate percentage of valid thermal colors
    total_pixels = image.shape[0] * image.shape[1]
    valid_pixels = np.count_nonzero(mask_combined)
    percentage_valid = (valid_pixels / total_pixels) * 100

    print(f"Valid Thermal Color Percentage: {percentage_valid:.2f}%")

    return percentage_valid >= min_valid_percentage

def predict_image(image_path, confidence_threshold=0.7):
    model_save_path = settings.MEDIA_ROOT + '/Dataset/crop_stress_model.h5'    
    model = load_model(model_save_path)

    # Class labels (update with your actual labels used during training)
    class_labels = ['BLB', 'BLAST', 'HEALTHY', 'HISPA', 'LEAF_SPOT']

    # Check color threshold before running the model
    if not check_color_threshold(image_path):
        print("Image does not match expected leaf colors. Returning 'Unknown'.")
        return "Unknown", 0.0

    # Preprocess the image
    image_array, image = preprocess_image(image_path, img_size=224)
    
    # Get predictions
    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions)
    predicted_class_label = class_labels[predicted_class_index]
    confidence = predictions[0][predicted_class_index]

    print(f"Predicted Class Index: {predicted_class_index}")
    print(f"Predicted Class Label: {predicted_class_label}")
    print(f"Prediction Confidence: {confidence:.2f}")

    # Check confidence level
    if confidence < confidence_threshold:
        return "Unknown", confidence

    return predicted_class_label, confidence
