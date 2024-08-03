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

> **_IMAGE PRE-PROCESSING_**

▶ Edge Detection: Edge detection is indirectly utilized through the use of the pre-trained license plate detection cascade (plate\_cascade). While the specific edge detection algorithm is not explicitly mentioned in the code, the detectMultiScale function of OpenCV’s CascadeClassifier class detects objects based on edges in the input image. This method inherently involves edge detection techniques to identify regions of interest (license plates) based on edge features.

▶Contour Tracing: Contour tracing is employed to highlight the boundaries of detected license plates. After detecting the regions of interest using the cascade classifier, the code draws rectangles around these regions, effectively outlining the contours of the license plates.

<p align="center">
<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/1*vC4KJWIBgOymEOW53JW-yg.jpeg" alt="Image 3">
</p>
<br>

To be continued..





.
.
.
.
.
.
.
.


### Scanning a number plate

![Screenshot of the web page scanning number plate](https://github.com/anuragaryanyt/number_plate_detections/blob/main/ss/Screenshot%20from%202024-03-28%2001-22-04.png?raw=true)

### Scanned image result

![Ss of scanned result](https://github.com/anuragaryanyt/number_plate_detections/blob/main/ss/Screenshot%20from%202024-03-28%2001-24-27.png?raw=true)

### Adding new vehicle details

![ss of new vehicle](https://github.com/anuragaryanyt/number_plate_detections/blob/main/ss/Screenshot%20from%202024-03-28%2001-24-06.png?raw=true)

### History of scanned vehicle's data (24 hours)

![ss of history](https://github.com/anuragaryanyt/number_plate_detections/blob/main/ss/Screenshot%20from%202024-03-28%2001-24-13.png?raw=true)

### All Vehicle Records

![ss of all vehicle records](https://github.com/anuragaryanyt/number_plate_detections/blob/main/ss/Screenshot%20from%202024-03-28%2001-24-18.png?raw=true)
