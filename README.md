# YOLOv8 Object Detection and Tracking with Flask Web Application

This project uses “YOLOv8” for real-time object detection and tracking within a video, with a Flask web application to upload videos, process them, and view/download the results. The solution also includes object counting (global and region-wise) and basic speed estimation for tracked objects.
We can use the dataset that is publicly available like MOT20,VisDrone or custom surveillance/CCTV video. The focus is on objects such as pedestrians, vehicles, or bicycles in outdoor or indoor environments. In our system, we have used a publicly available outdoor video streams to detect the different types of vehicles, person, speed estimation and counting etc.

The application is designed to process the uploaded videos, detect and track objects, count the objects globally or per region, and estimate speeds. The final output is an annotated video, along with statistics related to object counts and speed.
The main components include the following:

•	Flask app initialization
•	Route definitions for uploading, processing, and displaying videos
•	YOLOv8 model loading
•	Video processing logic (e.g., drawing boxes, counting, tracking)

## Features
Launch the Flask Application

Running Using Docker
            Build the Docker image:
            Run the Docker container
 Upload a Video for Object Detection and Tracking
The server will start running YOLOv8 inference on the video. The video will be processed frame by frame, with the following tasks being performed:

o	Object Detection: Identifying objects within each frame.
o	Object Tracking: Tracking objects across frames.
o	Object Counting: Counting the total number of unique objects and objects per region (entry, exit, restricted areas).
o	Global object count:
      - Region-wise counts (entry, exit, restricted areas).
o	Speed Estimation: Calculating object speeds based on pixel displacement over time.
o	Real-time Viewing: View processed video with annotated bounding boxes and tracking IDs.
o	Dockerized: The entire app is containerized using Docker for easy deployment.
 ## Setup Instructions:
     ### Prerequisites
    - Python 3.x
    - Docker (for containerized deployment)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/app
    cd app
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. (Optional) If we want to use Docker, build the Docker image:
    ```bash
    docker build -t yolo-flask-app .
    ```
4. Run the Flask application:
    ```bash
    flask run
    ```
5. Access the app at `http://127.0.0.1:5000`.

### Docker Deployment

To run the app with Docker, use:
```bash
docker run -p 5000:5000 yolo-flask-app



