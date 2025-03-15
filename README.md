# SmartAttend

SmartAttend is a computer vision project designed to automate student attendance tracking through real-time face recognition. Built using OpenCV, Firebase, and the ```face-recognition library```, this system ensures quick and accurate marking of attendance by recognizing students' faces and updating their attendance in real-time.

## Key Features

* Instantly updates and syncs student attendance details with zero delay using Firebase's real-time database.
* Automatically generates and stores known face encodings into Firebase Storage, enabling fast retrieval and recognition during future sessions.
* Recognizes time elapsed between scans to prevent students from marking attendance consecutively within a defined time window.
* Upon recognition, the system displays precise details of each student, including name and student ID, ensuring accurate records.

## Getting Started

### Installation
```
git clone https://github.com/zw-weng/SmartAttend.git
```
### Installing Dependencies
```
pip install -r requirements.txt
```
