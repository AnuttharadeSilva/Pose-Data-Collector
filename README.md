# Pose Data Collector

Student pose data collecting tool 

## Dataset

### Link

[Student pose dataset](https://drive.google.com/drive/folders/1v_Ppay4fQDfqA133bTYmAEos3xlhPyQ3?usp=sharing)

### Dataset properties

- 2 data streams: RGB image stream, Landmark Data
- 6 student poses (Classes): Neutral, Yawning, In a call, Hands on cheek, Hands on head, Use phone
- 3 subjects in 4 different environments

### Landmark Data

The landmark data are extracted using [Google Mediapipe Holistic framework](https://google.github.io/mediapipe/solutions/holistic.html) and collected into seperate csv files.
Properties:
- Class label
- Image name
- 218 features : x,y,z coordinates and visibility property of 65 landmarks from left hand, right hand and pose models

## Using the tool

### Running the tool

````
git clone https://github.com/AnuttharadeSilva/Pose-Data-Collector.git
cd Pose-Data-Collector
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
mkdir datasets
flask run
````
### Collecting data

- Select a class from the drop down and press start
- Wait 30 seconds until capturing data from the webcam stream
(Press 'q' to stop video capture if needed)
- Repeat above steps for all classes
