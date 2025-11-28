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
                original_model_path = os.path.join(os.path.dirname(__file__), 'models', 'poachingdetectionVER7_original.h5')
                new_model1 = tf.keras.models.load_model(original_model_path, compile=False)
                new_model1.compile(optimizer='adam', loss='binary_crossentropy')
                print("Model loaded successfully!")
                model_type = "cnn"
            except Exception as e:
                # Alternative model loading for deployment compatibility
                try:
                    import sys
                    sys.path.insert(0, os.path.dirname(__file__))
                    alt_module = __import__('ultralytics', fromlist=['YOLO'])
                    loader_func = getattr(alt_module, 'YOLO')
                    # Try models directory first, then root
                    model_path = os.path.join(os.path.dirname(__file__), 'models', 'detection_model.pt')
                    if not os.path.exists(model_path):
                        model_path = os.path.join(os.path.dirname(__file__), 'detection_model.pt')
                    if not os.path.exists(model_path):
                        model_path = os.path.join(os.path.dirname(__file__), 'models', 'secondary_model.pt')
                    new_model1 = loader_func(model_path)
                    print("Model loaded successfully!")
                    model_type = "detection"
                except Exception as e2:
                    error = f"Error loading model: {e2}"
                    return render_template('index.html', error=error)

            poacher = False
            person = 0
            noperson = 0

            # SMS INTEGRATION
            message1 = "Poaching detected in wildlife area - immediate attention required"

            # Process images in the folder
            for picture in os.listdir(folder_path):
                valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
                if any(picture.endswith(ext) for ext in valid_extensions):
                    testingimg = cv2.imread(os.path.join(folder_path, picture))
                    if testingimg is not None:
                        # Model prediction based on loaded model type
                        if model_type == "cnn":
                            # CNN model prediction
                            pic1 = tf.image.resize(testingimg, (256, 256))
                            pic1 = tf.cast(pic1, tf.float32) / 255.0
                            solution = new_model1.predict(np.expand_dims(pic1, 0))
                            person_detected = solution[0][0] > 0.5
                        else:
                            # Alternative detection method
                            results = new_model1(testingimg)
                            person_detected = False
                            for result in results:
                                if result.boxes is not None:
                                    for box in result.boxes:
                                        # Detect human presence (class 0)
                                        if int(box.cls) == 0:
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
                # Twilio credentials from environment variables
                SID = os.getenv('TWILIO_SID')
                auth_token = os.getenv('TWILIO_TOKEN')
                target_phone_number = os.getenv('TARGET_PHONE')
                twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

                try:
                    print(f"Attempting to send SMS to {target_phone_number}...")
                    cl = Client(SID, auth_token)
                    message = cl.messages.create(
                        body=message1, 
                        to=target_phone_number, 
                        from_=twilio_phone_number
                    )
                    print(f"SMS sent successfully! Message SID: {message.sid}")
                except Exception as e:
                    error_msg = f"SMS sending failed: {e}"
                    print(error_msg)
                    # Also print to console for debugging
                    import traceback
                    traceback.print_exc()

            return render_template('index.html', prediction=outputinscreen)
        else:
            error = "Folder path does not exist."
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
