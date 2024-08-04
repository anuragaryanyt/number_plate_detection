Number Plate Detection System
=============================
<br>

> **_INTRODUCTION_**

In recent years, the integration of computer vision technologies with everyday applications has led to significant advancements in various fields, ranging from surveillance and security to transportation and automation. One such application is the development of a Number Plate Recognition System, which employs a combination of image processing techniques and optical character recognition (OCR) to automatically identify and recognize number plates in real-time video streams. This system holds immense potential for enhancing traffic management, law enforcement, and parking systems by providing efficient and accurate vehicle identification capabilities.

In recent years, the integration of computer vision technologies with everyday applications has led to significant advancements in various fields, ranging from surveillance and security to transportation and automation. One such application is the development of a Number Plate Recognition System, which employs a combination of image processing techniques and optical character recognition (OCR) to automatically identify and recognize number plates in real-time video streams. This system holds immense potential for enhancing traffic management, law enforcement, and parking systems by providing efficient and accurate vehicle identification capabilities.

<p align="center">
<img src="https://miro.medium.com/v2/resize:fit:640/format:webp/1*PvJgjxWWRmHptWJ4oIx0kw.png" alt="Image 1">
</p>

Key components of the Number Plate Recognition System include a Haar cascade classifier for number plate detection, Tesseract OCR for character recognition, and MongoDB for storing and managing vehicle information. The system architecture is designed to facilitate real-time processing of video streams, ensuring prompt identification of vehicles as they pass through the monitored area. Additionally, a user-friendly web interface built with Flask framework allows for functionalities such as adding new vehicles to the database and viewing recognized plate records.

This project aims to address several challenges associated with Number plate recognition, including variations in plate appearance due to factors such as lighting conditions, viewing angle, and occlusions. Advanced image processing techniques are employed to enhance the robustness and accuracy of plate detection and character recognition, thereby improving the overall performance of the system. Furthermore, the integration of user authentication mechanisms ensures secure access to system functionalities, preventing unauthorized users from tampering with the database or system settings.

<br>

> **_SYSTEM COMPONENTS_**

▶ Python: Programming language used for system development. Provides flexibility, ease of use, and extensive libraries for image processing.

▶ OpenCV (Open Source Computer Vision Library): Integral for image and video processing tasks. Facilitates license plate detection and optical character recognition (OCR).

▶ Flask: Web framework for building the user interface. Enables communication between the backend and frontend components.

▶ MongoDB: NoSQL database used for storing recognized plate information. Provides scalability, flexibility, and compatibility with Python-based applications.

<br>

> **_WORK FLOW_**

<p align="center">
<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*C8qzrtGpj91bo9jCuDOVZA.png" alt="Image 2">
</p>

<br>

> **_SYSTEM ARCHITECTURE_**

<p align="center">
<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*kMaNzQJ7d-6RM7upI0KTGw.png" alt="Image 1">
</p>

<br>

> **_IMAGE PRE-PROCESSING_**

▶ Edge Detection: Edge detection is indirectly utilized through the use of the pre-trained license plate detection cascade (plate\_cascade). While the specific edge detection algorithm is not explicitly mentioned in the code, the detectMultiScale function of OpenCV’s CascadeClassifier class detects objects based on edges in the input image. This method inherently involves edge detection techniques to identify regions of interest (license plates) based on edge features.

▶Contour Tracing: Contour tracing is employed to highlight the boundaries of detected license plates. After detecting the regions of interest using the cascade classifier, the code draws rectangles around these regions, effectively outlining the contours of the license plates.

<p align="center">
<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*vC4KJWIBgOymEOW53JW-yg.jpeg" alt="Image 3">
</p>

<br>

> **_LIBRARIES_**

Install all the libraries and required dependencies.

```
import os  
from unittest import result  
import cv2  
from datetime import datetime, timedelta, timezone  
import pytesseract  
import requests  
from PIL import Image  
from flask import Flask, jsonify, redirect, render\_template, Response, request, session, url\_for  
import threading  
from pymongo import MongoClient
```
<br>


> **_DATABASE CONNECTION_**

The application connects to a MongoDB database. MongoDB Atlas is used for cloud-hosted MongoDB, allowing easy scaling and management.

```
client = MongoClient("<mongodb server url>")  
db = client['vehicle_database']  
vehicles_collection = db['vehicle']  
history_collection = db['history']
```

The `vehicles_collection` stores vehicle details, while the `history_collection` logs detected plates and their timestamps.

<br>

> **_LOADING VEHICLE DATABASE_**

```
def load_vehicle_database():  
    database = {}  
    vehicles_collection = db['vehicle']  
    for vehicle in vehicles_collection.find():  
        plate_number = vehicle['plate_number']  
        database[plate_number] = {  
            "owner_name": vehicle['owner_name'],  
            "make": vehicle['make'],  
            "model": vehicle['model'],  
            "color": vehicle['color']  
        }  
    print("Vehicle database loaded successfully.")  
    return database  
  
vehicle_database = load_vehicle_database()
```

This function queries all vehicle records from MongoDB and stores them in a dictionary where the plate number is the key.

<br>

> **_VIDEO PROCESSING_**

The `process_video` function captures video frames from the camera, detects license plates using OpenCV, and performs OCR using Tesseract to recognize the plate numbers.

<br>

1\.  **Load Cascade for Plate Detection:** The Haar Cascade classifier is pre-trained to detect license plates.

```
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
```

2\. **Configure Tesseract OCR:** Specifies the path to the Tesseract executable.

```
# for ubuntu
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# for windows paste the path where it is installed
```

3\. **Define OCR Function:**

```
def perform_ocr(img):
    custom_config = r'--oem 3 --psm 6'
    plate_number = pytesseract.image_to_string(img, config=custom_config)
    return plate_number.strip()
```

4\. **Process Video Frames:**

```
def process_video():
    cap = cv2.VideoCapture(-1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in plates:
            plate_roi = frame[y:y + h, x:x + w]
            pil_image = Image.fromarray(cv2.cvtColor(plate_roi, cv2.COLOR_BGR2RGB))
            plate_number = perform_ocr(pil_image)
            if plate_number in vehicle_database:
                vehicle_info = vehicle_database[plate_number]
                if plate_number not in [plate['plate_number'] for plate in recognized_plates]:
                    timestamp = datetime.now()
                    recognized_plates.append({
                        "plate_number": plate_number,
                        "owner_name": vehicle_info['owner_name'],
                        "make": vehicle_info['make'],
                        "model": vehicle_info['model'],
                        "color": vehicle_info['color'],
                        "timestamp": timestamp
                    })
                    history_collection.insert_one({
                        "plate_number": plate_number,
                        "owner_name": vehicle_info['owner_name'],
                        "make": vehicle_info['make'],
                        "model": vehicle_info['model'],
                        "color": vehicle_info['color'],
                        "timestamp": timestamp
                    })
                info_text = f"Owner: {vehicle_info['owner_name']}, Make: {vehicle_info['make']}, Model: {vehicle_info['model']}, Color: {vehicle_info['color']}"
                cv2.putText(frame, info_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
    cap.release()
```
<br>

![Screenshot from 2024-03-28 01-22-04](https://github.com/user-attachments/assets/39663a93-9adc-4eaa-b553-183169265322)



*   Captures video frames and converts them to grayscale.
*   Detects license plates in the frame using the Haar Cascade classifier.
*   Extracts the region of interest (ROI) and performs OCR to get the plate number.
*   Matches the recognized plate number with the database and logs the information if it’s a new recognition.
*   Annotates the frame with vehicle information and the detected plate.

<br>

> **_VIDEO STREAMING_**


```
@app.route('/video_feed')
def video_feed():
    return Response(process_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
```

The `video_feed` route returns a video stream using the `process_video` generator function.

<br>

> **_USER AUTHENTICATION_**

Basic user authentication is implemented to restrict access to certain routes. The login system uses Flask’s session management to keep track of logged-in users.

1.  Define Admin Credentials
2.  Login Route
3.  Logout Route

<br>

> **_VEHICLE RECORD MANAGEMENT_**

1.  **Add Vehicle Route:**

```
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    plate_number = request.form['plate_number']
    owner_name = request.form['owner_name']
    make = request.form['make']
    model = request.form['model']
    color = request.form['color']
    vehicles_collection.insert_one({
        "plate_number": plate_number,
        "owner_name": owner_name,
        "make": make,
        "model": model,
        "color": color
    })
    return redirect(url_for('index'))
```

![Screenshot from 2024-03-28 01-24-06](https://github.com/user-attachments/assets/4aa25c86-3103-49c9-8f8e-69acc45f5bd7)



2\. **Recognized Plates Route:**

```
@app.route('/recognized_plates')
def recognized_plates_page():
    return render_template('recognized_plates.html', recognized_plates=recognized_plates)
```

![Screenshot from 2024-03-28 01-24-27](https://github.com/user-attachments/assets/1a510c7b-d882-44e2-b127-7b16c9d981e3)



<br>

> **_DISPLAYING DATA_**

The application provides a dashboard to display recognized plates and vehicle records.

1.  **Index Route:**

```
@app.route('/index')
def index():
    try:
        past_24_hours = datetime.now() - timedelta(hours=24)
        data = history_collection.find({"timestamp": {"$gte": past_24_hours}})
        return render_template('index.html', data=data)
    except Exception as e:
        app.logger.error(f"An error occurred while fetching data from the database: {e}")
        return "An error occurred while fetching data from the database. Please check the logs for more information."
```

2\. **Records Route:**

```
@app.route('/records')
def records():
    try:
        database = {}
        records_collection = db['vehicle']
        database = records_collection.find()
        app.logger.info("Records fetched successfully")
        return render_template('records.html', rec=database)
    except Exception as e:
        app.logger.error(f"An error occurred while fetching records from the database: {e}")
        return "An error occurred while fetching records from the database. Please check the logs for more information."
```

The `index` route displays recognized plates within the past 24 hours, while the `records` route displays all vehicle records.

![Screenshot from 2024-03-28 01-24-13](https://github.com/user-attachments/assets/1bd4596e-5f85-4659-8a0d-8a795820b5af)



<br>

> **_RUNNING THE APPLICATION_**

The Flask application is started, and video processing is run in a separate thread to avoid blocking the main thread.

```
def run_video_processing():
    with app.app_context():
        app.video_thread = threading.Thread(target=process_video)
        app.video_thread.start()

if __name__ == '__main__':
    run_video_processing()
    app.run(debug=True)
```

The `run_video_processing` function initializes and starts the video processing thread, ensuring the application remains responsive while processing video frames.


<br>

> **_CONCLUSION_**

This number plate detection system integrates real-time video processing with a web-based interface, leveraging OpenCV, Tesseract OCR, and MongoDB. It demonstrates the practical application of computer vision and web technologies for automated license plate recognition and vehicle management.

