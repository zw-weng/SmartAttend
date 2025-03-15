# SmartAttend

SmartAttend is a computer vision project designed to automate student attendance tracking through real-time face recognition. Built using OpenCV, Firebase, and the ```face-recognition library```, this system ensures quick and accurate marking of attendance by recognizing students' faces and updating their attendance in real-time.

## Key Features
✅ Real-time Face Recognition – Detects and recognizes student faces instantly using OpenCV and the face-recognition library.<br>
✅ Instant Attendance Updates – Syncs student attendance with Firebase Realtime Database with zero delay.<br>
✅ Face Encoding & Storage – Stores face encodings in Firebase Storage for future retrieval.<br>
✅ Duplicate Prevention – Recognizes time elapsed between scans to prevent duplicate attendance entries.<br>
✅ Student Info Display – Shows student name, ID, major, and attendance count on successful recognition.<br>

## Getting Started
### Clone the repository
```
git clone https://github.com/yourusername/SmartAttend.git
cd SmartAttend
```
### Install dependencies
```
pip install -r requirements.txt
```
### Firebase setup
- Create a Firebase Project
- Download serviceAccountKey.json from Firebase
- Set Up Firebase Realtime Database
- Set Up Firebase Storage
### Run the encoding script
- Add your image into Image folder
```
python encode_faces.py
```
### Run the database script
- Add your data into database.py
```
python database.py
```
### Start the GUI
```
python main.py
```
## GUI Demo
![SmartAttend Sample](https://github.com/zw-weng/SmartAttend/blob/main/sample.png)
