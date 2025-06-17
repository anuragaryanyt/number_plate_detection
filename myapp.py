import os
from unittest import result
import cv2
from datetime import datetime, timedelta, timezone
import pytesseract
import requests
from PIL import Image
from flask import Flask, jsonify, redirect, render_template, Response, request, session, url_for
import threading
from pymongo import MongoClient

app = Flask(__name__)

# @app.after_request
# def allow_camera(resp):
#     resp.headers['Permissions-Policy'] = 'camera=(self)'
#     return resp

# Connect to local host MongoDB

# client = MongoClient('mongodb://localhost:27017/')
# db= client.vehicle

client = MongoClient("mongodb+srv://vehicle:1234@atlascluster.uczqi01.mongodb.net/")
db = client['vehicle_database']

vehicles_collection = db['vehicle']  #collection name   
history_collection = db['history'] #collection name

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

# for checking only whether it is printing the data or not
# print("Retrieved data from MongoDB:")
# for plate_number, vehicle_info in vehicle_database.items():
#     print(f"Plate Number: {plate_number}")
#     print(f"Owner Name: {vehicle_info['owner_name']}")
#     print(f"Make: {vehicle_info['make']}")
#     print(f"Model: {vehicle_info['model']}")
#     print(f"Color: {vehicle_info['color']}")
#     print("-" * 20)
#     print("-" * 20)


# List to store recognized license plate information
recognized_plates = []

# Load the pre-trained license plate detection cascade
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Function to perform OCR on an image region
def perform_ocr(img):
    custom_config = r'--oem 3 --psm 6'  # OCR engine mode and page segmentation mode
    plate_number = pytesseract.image_to_string(img, config=custom_config)
    return plate_number.strip()

# Function to process the video stream
def process_video():
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(-1)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect license plates in the frame
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in plates:
            # Crop the region of interest (ROI) containing the license plate
            plate_roi = frame[y:y + h, x:x + w]

            # Perform OCR on the license plate region
            pil_image = Image.fromarray(cv2.cvtColor(plate_roi, cv2.COLOR_BGR2RGB))
            plate_number = perform_ocr(pil_image)

            # Match the plate number with the database
            if plate_number in vehicle_database:
                vehicle_info = vehicle_database[plate_number]

                # Check if the plate is already recognized
                if plate_number not in [plate['plate_number'] for plate in recognized_plates]:
                    # Store the recognized plate information in the list
                    # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    timestamp = datetime.now()

            
                    recognized_plates.append({
                        "plate_number": plate_number,
                        "owner_name": vehicle_info['owner_name'],
                        "make": vehicle_info['make'],
                        "model": vehicle_info['model'],
                        "color": vehicle_info['color'],
                        "timestamp": timestamp
                    })

                    # history_collection = db['history']
                    history_collection.insert_one({
                        "plate_number": plate_number,
                        "owner_name": vehicle_info['owner_name'],
                        "make": vehicle_info['make'],
                        "model": vehicle_info['model'],
                        "color": vehicle_info['color'],
                        "timestamp": timestamp
                    })

                # Display the vehicle information on the frame including owner name
                info_text = f"Owner: {vehicle_info['owner_name']}, Make: {vehicle_info['make']}, Model: {vehicle_info['model']}, Color: {vehicle_info['color']}"
                cv2.putText(frame, info_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the original frame with the license plate highlighted
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the processed frame
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

    pass

# Function to run the video processing in a separate thread
def run_video_processing():
    with app.app_context():
        app.video_thread = threading.Thread(target=process_video)
        app.video_thread.start()
    # Your existing code for running video processing
    pass

def get_utc_now():
    return datetime.now(timezone.utc)


@app.route('/video_feed')
def video_feed():
    return Response(process_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


#login function
app.secret_key = 'admin'  # Add a secret key for session management

# Define admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

# Add a login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Set session variable indicating user is logged in
            return redirect(url_for('index'))  # Redirect to index.html
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear session variable
    return redirect(url_for('index'))


@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():

    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    plate_number = request.form['plate_number']
    owner_name = request.form['owner_name']
    make = request.form['make']
    model = request.form['model']
    color = request.form['color']

    # Insert the new vehicle information into the MongoDB database
    
    vehicles_collection.insert_one({
        "plate_number": plate_number,
        "owner_name": owner_name,
        "make": make,
        "model": model,
        "color": color
    })
    return redirect(url_for('index'))
    # return redirect(url_for('add_vehicle'))

@app.route('/recognized_plates')
def recognized_plates_page():
    return render_template('recognized_plates.html', recognized_plates=recognized_plates)


@app.route('/index')
def index():
    try:
        # Calculate the timestamp for 24 hours ago   
        past_24_hours = datetime.now() - timedelta(hours=24)
        
        # Query the history collection for documents within the past 24 hours
        data = history_collection.find({"timestamp": {"$gte": past_24_hours}})
        
        return render_template('index.html', data=data)
        # return render_template('index.html', data=database)
    
    except Exception as e:
        app.logger.error(f"An error occurred while fetching data from the database: {e}")
        return "An error occurred while fetching data from the database. Please check the logs for more information."
    

@app.route('/records')
def records():

    try:
        database = {}
        records_collection = db['vehicle']
        database = records_collection.find()

        # Logging successful fetch
        app.logger.info("Records fetched successfully")

        # Returning the database for rendering in the template
        return render_template('records.html', rec=database)

    except Exception as e:
        app.logger.error(f"An error occurred while fetching records from the database: {e}")
        return "An error occurred while fetching records from the database. Please check the logs for more information."


if __name__ == '__main__':
    run_video_processing()
    app.run(debug=True)


