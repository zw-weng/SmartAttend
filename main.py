import cv2
import os
import pickle
import face_recognition as fr
import numpy as np
import cvzone
from datetime import datetime
from firebase_setup import firebase_db, firebase_storage

# Webcam settings
cap = cv2.VideoCapture(0)  # Default webcam
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Load background image
bgImg = cv2.imread('Resources/background.png')

# Load mode images
modesPath = 'Resources/Modes'
modesImgList = [cv2.imread(os.path.join(modesPath, path)) for path in os.listdir(modesPath)]

# Load encoded file
with open('encodedFile.p', 'rb') as file:
    encodeList, studentId = pickle.load(file)

# Initialize state variables
modeType, cnt, id, stdImg = 0, 0, 0, None

while True:
    success, frame = cap.read()
    if not success:
        print("Error: Failed to capture frame.")
        continue

    # Resize frame to improve performance
    smallFrame = cv2.cvtColor(cv2.resize(frame, (0, 0), None, 0.25, 0.25), cv2.COLOR_BGR2RGB)

    # Detect faces and encode them
    faceCurrFrame = fr.face_locations(smallFrame)
    encodeCurrFrame = fr.face_encodings(smallFrame, faceCurrFrame, num_jitters=1)

    # Update background
    bgImg[162:162 + 480, 55:55 + 640] = frame
    bgImg[44:44 + 633, 808:808 + 414] = modesImgList[modeType]

    for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
        matches = fr.compare_faces(encodeList, encodeFace)
        faceDist = fr.face_distance(encodeList, encodeFace)
        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            # Draw rectangle around recognized face
            y1, x2, y2, x1 = [v * 4 for v in faceLoc]  # Scale back
            bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
            cvzone.cornerRect(bgImg, bbox, rt=0, colorR=(135, 45, 74))

            id = studentId[matchIndex]
            print("Student detected:", id)

            if cnt == 0:  # First detection
                cvzone.putTextRect(bgImg, 'Loading...', (55 + x1 + 10, 162 + y1 - 10))
                cv2.imshow("SmartAttend", bgImg)
                cv2.waitKey(1)
                cnt = 1
                modeType = 1

    if cnt != 0:
        if cnt == 1:
            # Fetch student details from Firebase
            stdInfo = firebase_db.reference(f'Students/{id}').get()
            if stdInfo:
                print(stdInfo)

                # Fetch student image from Firebase Storage
                bucket = firebase_storage.bucket()
                blob = bucket.get_blob(f'Images/{id}.png')
                if blob:
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    stdImg = cv2.imdecode(array, cv2.IMREAD_COLOR)

                # Attendance logic
                last_attendance = datetime.strptime(stdInfo['latest_attendance'], "%Y-%m-%d %H:%M:%S")
                duration = (datetime.now() - last_attendance).total_seconds()

                if duration > 30:
                    stdInfo['tot_attendance'] += 1
                    ref = firebase_db.reference(f'Students/{id}')
                    ref.child('tot_attendance').set(stdInfo['tot_attendance'])
                    ref.child('latest_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    cnt = 0
                    bgImg[44:44 + 633, 808:808 + 414] = modesImgList[modeType]

        if modeType != 3:
            modeType = 2 if 10 < cnt <= 20 else modeType
            bgImg[44:44 + 633, 808:808 + 414] = modesImgList[modeType]

            if cnt <= 10 and stdInfo:
                # Display student info
                cv2.putText(bgImg, str(stdInfo['tot_attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(bgImg, str(id), (1003, 493), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(bgImg, str(stdInfo['major']), (1003, 552), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(bgImg, str(stdInfo['cgpa']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(bgImg, str(stdInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(bgImg, str(stdInfo['cohort']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                (width, height), _ = cv2.getTextSize(stdInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                center_offset = (414 - width) // 2
                cv2.putText(bgImg, str(stdInfo['name']), (808 + center_offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                if stdImg is not None:
                    bgImg[175:175 + 216, 909:909 + 216] = stdImg

            cnt += 1
            if cnt >= 20:
                cnt, modeType, stdInfo, stdImg = 0, 0, None, None
                bgImg[44:44 + 633, 808:808 + 414] = modesImgList[modeType]

    else:
        modeType, cnt = 0, 0

    cv2.imshow("SmartAttend", bgImg)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()