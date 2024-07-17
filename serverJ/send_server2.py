"""
import json
from ultralytics import YOLO
from PIL import Image
import requests

# Load the trained model
model_path = "C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/PDD_Phase2_V3.pt"
model = YOLO(model_path)

def predict_and_return(image_path):
    try:
        # Load the image
        img = Image.open(image_path)

        # Perform the prediction
        results = model.predict(image_path, conf=0.10, iou=0.50)
        predictions = results[0].boxes.data.tolist()  # Update to match the output format of your model

        formatted_predictions = []
        for pred in predictions:
            formatted_predictions.append({
                'class_name': int(pred[-1]),  # Assuming the class name is the last element
                'confidence': float(pred[-2])  # Assuming the confidence score is the second to last element
            })

        return formatted_predictions
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return []

def send_predictions(predictions):
    url = "http://192.168.8.144:8000/save_predictions/"
    data = {"predictions": predictions}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(f"Predictions successfully sent. Server response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send predictions: {e}")

# Example usage
if __name__ == "__main__":
    image_path = 'C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/Test images/1.jpg'
    results = predict_and_return(image_path)
    if results:
        send_predictions(results)
"""
import json
from ultralytics import YOLO
from PIL import Image
import requests

# Load the trained model
model_path = "C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/PDD_Phase2_V3.pt"
model = YOLO(model_path)

class_names = ['Early Blight', 'Healthy', 'Late Blight']  # Replace with your actual class names

def predict_and_return(image_path):
    try:
        # Load the image
        img = Image.open(image_path)

        # Perform the prediction
        results = model.predict(image_path, conf=0.10, iou=0.50)
        predictions = results[0].boxes.data.tolist()  # Update to match the output format of your model

        formatted_predictions = []
        for pred in predictions:
            class_id = int(pred[-1])
            class_name = class_names[class_id]
            formatted_predictions.append({
                'class_name': class_name,
                'confidence': float(pred[-2])  # Assuming the confidence score is the second to last element
            })

        return formatted_predictions
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return []

def send_predictions(predictions):
    url = "http://192.168.8.144:8000/save_predictions/"
    data = {"predictions": predictions}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(f"Predictions successfully sent. Server response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send predictions: {e}")

# Example usage
if __name__ == "__main__":
    image_path = 'C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/Test images/1.jpg'
    results = predict_and_return(image_path)
    if results:
        send_predictions(results)