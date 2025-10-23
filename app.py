import os
from flask import Flask, render_template, request
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import CategoricalCrossentropy
from twilio.rest import Client
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_folder():
    if request.method == 'POST':
        folder_path = request.form['folder_path']  # Get user input for folder path
        if os.path.exists(folder_path):  # Check if the folder exists
            # Load the machine learning model
            try:
                # Try to load the original CNN model first, fallback to backup if it fails
                try:
                    # Try original model first
                    original_model_path = os.path.join(os.path.dirname(__file__), 'models', 'poachingdetectionVER7_original.h5')
                    new_model1 = tf.keras.models.load_model(original_model_path, compile=False)
                    new_model1.compile(optimizer='adam', loss='binary_crossentropy')
                    print("Original CNN model loaded successfully!")
                    model_type = "cnn"
                except Exception as e:
                    print(f"Original model failed: {e}")
                    # Fallback to backup detection system
                    from ultralytics import YOLO
                    new_model1 = YOLO('yolov8n.pt')
                    print("Backup detection system loaded successfully!")
                    model_type = "yolo"
                    
            except Exception as e:
                error = f"Error loading model: {e}"
                return render_template('index.html', error=error)

            poacher = False
            person = 0
            noperson = 0

            # SMS INTEGRATION
            try:
                response = requests.get("http://ip-api.com/json/", timeout=5).json()
                message1 = f"The region of poaching is {response['region']} {response['city']} latitude is {response['lat']} longitude is {response['lon']}"
            except requests.exceptions.RequestException as e:
                print(f"Location retrieval failed: {e}")
                message1 = "Poaching detected in wildlife area - immediate attention required"

            # Process images in the folder
            for picture in os.listdir(folder_path):
                valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
                if any(picture.endswith(ext) for ext in valid_extensions):
                    testingimg = cv2.imread(os.path.join(folder_path, picture))
                    if testingimg is not None:
                        # Use appropriate model for detection
                        if model_type == "cnn":
                            # CNN model prediction
                            pic1 = tf.image.resize(testingimg, (256, 256))
                            pic1 = tf.cast(pic1, tf.float32) / 255.0
                            solution = new_model1.predict(np.expand_dims(pic1, 0))
                            person_detected = solution[0][0] > 0.5
                        else:
                            # Backup detection system prediction
                            results = new_model1(testingimg)
                            person_detected = False
                            for result in results:
                                if result.boxes is not None:
                                    for box in result.boxes:
                                        # Class 0 is 'person' in detection system
                                        if int(box.cls) == 0:  # person class
                                            person_detected = True
                                            break

                        if person_detected:
                            print(f'Poacher is present warning: {picture}')
                            poacher = True
                            person += 1
                        else:
                            print(f'No poacher is present: {picture}')
                            noperson += 1
                    else:
                        print(f"Error loading image: {picture}")
            
            # Send SMS if poaching is detected
            finalmessage = person > (person + noperson) * 0.10
            outputinscreen = "Poaching is present and SMS regarding poaching is sent to concerned authorities" if finalmessage else "Poaching is not present and animals are safe"

            if finalmessage and poacher:
                # Twilio credentials - USE ENVIRONMENT VARIABLES ONLY
                SID = os.getenv('TWILIO_SID', 'your_twilio_sid')
                auth_token = os.getenv('TWILIO_TOKEN', 'your_twilio_token')
                target_phone_number = os.getenv('TARGET_PHONE', '+1234567890')
                messaging_service_sid = os.getenv('TWILIO_SERVICE_SID', 'your_messaging_service_sid')

                try:
                    cl = Client(SID, auth_token)
                    cl.messages.create(body=message1, to=target_phone_number, messaging_service_sid=messaging_service_sid)
                except Exception as e:
                    print(f"SMS sending failed: {e}")

            return render_template('index.html', prediction=outputinscreen)
        else:
            error = "Folder path does not exist."
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
