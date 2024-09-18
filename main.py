import cv2
import os
import pickle
import face_recognition as fr
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartattend-9e9f9-default-rtdb.firebaseio.com/',
    'storageBucket': 'smartattend-9e9f9.appspot.com'
})

# Webcam settings
cap = cv2.VideoCapture(0)   # default webcam
cap.set(3, 640) # width
cap.set(4, 480) # height

# Get images from Resources
bgImg = cv2.imread('Resources/background.png')
modesPath = 'Resources/Modes'
modesPathList = os.listdir(modesPath)
modesImgList = []

for path in modesPathList:
    modesImgList.append(cv2.imread(os.path.join(modesPath, path)))

# Load encoded file
file = open('encodedFile.p', 'rb')
encodeListWithId = pickle.load(file)
file.close()

encodeList, studentId = encodeListWithId
# print(studentId)

modeType = 0
cnt = 0
id = 0
stdImg = []

while True:
    success, frame = cap.read()
    
    # Resize frame from webcam to 1/4 of its actual size
    # Reduce computational load
    smallFrame = cv2.cvtColor(cv2.resize(frame, (0,0), None, 0.25, 0.25), cv2.COLOR_BGR2RGB)
    
    # Find the face and encode it
    faceCurrFrame = fr.face_locations(smallFrame)
    encodeCurrFrame = fr.face_encodings(smallFrame, faceCurrFrame, num_jitters=1) # reduce computational load
    
    bgImg[162:162+480, 55:55+640] = frame
    bgImg[44:44+633, 808:808+414] = modesImgList[modeType]
    
    for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
        matches = fr.compare_faces(encodeList, encodeFace)
        faceDist = fr.face_distance(encodeList, encodeFace) # lower score, higher match
        matchIndex = np.argmin(faceDist)
        # print("Matches", matches)
        # print("FaceDist", faceDist)
        # print("Match index", matchIndex)
        
        if matches[matchIndex]:
            # Draw a rectangle around our face
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 # multiply by 4 as we reduce its size by 4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            bgImg = bgImg = cvzone.cornerRect(bgImg, bbox, rt=0, colorR=(135, 45, 74))
            
            id = studentId[matchIndex]
            print("Student detected:", studentId[matchIndex])
            
            if cnt == 0: # get 1st recognized face
                text_position = (55 + x1 + 10, 162 + y1 - 10)
                cvzone.putTextRect(bgImg, 'Loading...', text_position)
                cv2.imshow("SmartAttend", bgImg)
                cv2.waitKey(1)
                cnt = 1
                modeType = 1
            
    if cnt != 0:
        if cnt == 1:
            # Get data from firebase db
            stdInfo = db.reference(f'Students/{id}').get()
            print(stdInfo)
            
            # Get image from firebase storage
            bucket = storage.bucket()
            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            stdImg = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            # Check attendance
            datetimeObject = datetime.strptime(stdInfo['latest_attendance'], "%Y-%m-%d %H:%M:%S")
            duration = (datetime.now() - datetimeObject).total_seconds()
            
            if duration > 30:
                # Update attendance
                ref = db.reference(f'Students/{id}')
                stdInfo['tot_attendance'] += 1
                ref.child('tot_attendance').set(stdInfo['tot_attendance'])
                ref.child('latest_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType = 3
                cnt = 0
                bgImg[44:44+633, 808:808+414] = modesImgList[modeType]
        
        if modeType != 3:
            if 10 < cnt <= 20:
                modeType = 2
            
            bgImg[44:44+633, 808:808+414] = modesImgList[modeType]
                
            if cnt <= 10:
                cv2.putText(bgImg, str(stdInfo['tot_attendance']), (861,125), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                cv2.putText(bgImg, str(id), (1003,493), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                cv2.putText(bgImg, str(stdInfo['major']), (1003,552), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                cv2.putText(bgImg, str(stdInfo['cgpa']), (910,625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                cv2.putText(bgImg, str(stdInfo['year']), (1025,625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                cv2.putText(bgImg, str(stdInfo['cohort']), (1125,625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                
                (width, height), _ = cv2.getTextSize(stdInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                center_offset = (414 - width) // 2
                cv2.putText(bgImg, str(stdInfo['name']), (808 + center_offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,50), 1)
                
                bgImg[175:175+216, 909:909+216] = stdImg
        
            cnt += 1
            
            if cnt >= 20:
                cnt = 0
                modeType = 0
                stdInfo = []
                stdImg = []
                bgImg[44:44+633, 808:808+414] = modesImgList[modeType]
    
    else:
        modeType = 0
        cnt = 0
    
    cv2.imshow("SmartAttend", bgImg)
    
    # Press 'q' to break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()