import json
from ultralytics import YOLO
import os
from PIL import Image
import matplotlib.pyplot as plt

# Load the trained model
model_path = "C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/PDD_Phase2_V3.pt"
model = YOLO(model_path)

def predict_and_send(image_path):
    try:
        # Load the image
        img = Image.open(image_path)

        # Perform the prediction
        results = model.predict(image_path, conf=0.10, iou=0.50)
        prediction = results[0].tojson()

        # Parse the JSON string to a dictionary
        prediction_dict = json.loads(prediction)

        # Extract predictions
        predictions = prediction_dict

        # Format predictions for server
        formatted_predictions = [{
            'class_name': det['name'],
            'confidence': det['confidence']
        } for det in predictions]

        # Display the image
        plt.imshow(img)
        plt.axis('off')
        plt.title('Predicted Image')
        plt.show()

        return formatted_predictions
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return []

# Path to the image you want to predict
image_path = 'C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/Test images/1.jpg'

# Make prediction and print results
if __name__ == "__main__":
    results = predict_and_send(image_path)
    for det in results:
        print(f"Class: {det['class_name']}, Confidence: {det['confidence']:.2f}")
