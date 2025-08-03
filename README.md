 README.md
markdown
Copy
Edit
# 🦏 Poaching Detection using CNN Model

A deep learning-powered Flask web application that detects wildlife poaching activities in images using a trained CNN model. If poaching is detected in a significant percentage of uploaded images, a real-time alert is sent to authorities via Twilio SMS.

---

## 📸 Demo

> Upload a folder containing wildlife surveillance images. The model will:
- Classify each image as **"poacher present"** or **"no poacher"**
- Display overall results on the frontend
- Trigger an SMS alert if poaching is detected above a defined threshold

---

## 🚀 Features

- 🧠 CNN-based binary image classification
- 🗂️ Folder-based image upload and batch processing
- 📍 IP-based location detection for SMS alert
- 📱 Twilio integration for instant poaching alerts
- ⚡ Lightweight Flask backend with HTML/CSS frontend
- 🔐 Environment variable support for secrets

---

## 📦 Tech Stack

| Tool/Library        | Purpose                            |
|---------------------|-------------------------------------|
| Python              | Core programming language           |
| Flask               | Web framework (backend)             |
| TensorFlow / Keras  | CNN model loading and inference     |
| OpenCV / NumPy      | Image processing                    |
| Twilio API          | SMS alert system                    |
| dotenv              | Secure environment variable loading |

---

## 🖼️ Model Info

- Model type: Convolutional Neural Network (CNN)
- Input size: 256x256 images
- Output: Binary classification (`poacher` / `no poacher`)
- File: `poachingdetectionVER7.h5`

---

## 🧪 Folder Structure

project/
│
├── app.py
├── poachingdetectionVER7.h5
├── templates/
│ └── index.html
├── static/
│ └── css/
│ └── style.css
├── .env
├── .gitignore
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/suryakirank1/Poaching-Detection-using-CNN-model.git
cd Poaching-Detection-using-CNN-model
2️⃣ Setup Virtual Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On macOS/Linux
3️⃣ Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Configure Environment Variables
Create a .env file:

ini
Copy
Edit
TWILIO_SID=your_twilio_sid
TWILIO_TOKEN=your_twilio_auth_token
TWILIO_SERVICE_SID=your_twilio_msg_service_sid
TARGET_PHONE=+91xxxxxxxxxx
✅ Make sure .env is listed in .gitignore

▶️ Run the App
bash
Copy
Edit
python app.py
Then visit: http://127.0.0.1:5000

📧 SMS Trigger Conditions
If more than 10% of the images are detected to contain a poacher, a message is sent via Twilio containing:

Detected city and region

Latitude and longitude (via IP lookup)

Poaching warning

🔐 Security Note
Do not commit your Twilio credentials or .env file to GitHub.
Use .gitignore to prevent secrets from being pushed.

🧠 Future Enhancements
 Live camera feed analysis

 Logging and dashboard integration

 Multiclass classification (poacher, ranger, animal, etc.)

 Deploy on cloud platforms (Render, HuggingFace Spaces, etc.)

🙏 Acknowledgements
Twilio

TensorFlow

IP-API

Flask

📜 License
This project is for educational purposes. You are free to modify and use it under the MIT License.

