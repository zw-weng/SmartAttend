import cv2
import face_recognition as fr
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartattend-9e9f9-default-rtdb.firebaseio.com/',
    'storageBucket': 'smartattend-9e9f9.appspot.com'
})

# Import student images
imgPath = 'Images'
imgPathList = os.listdir(imgPath)
imgList = []

studentId = []

for path in imgPathList:
    imgList.append(cv2.imread(os.path.join(imgPath, path)))
    
    # Extract student id from .png
    studentId.append(os.path.splitext(path)[0]) # taking 1st element
    
    # Upload image folder to firebase
    fileName = f'{imgPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
def encoding(images):
    encodeList = []
    
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # change from bgr to rgb
        face = fr.face_encodings(img)
        
        if face:
            encode = face[0] # get 1st face encoding
            encodeList.append(encode)
        else:
            print("No face detected in the image")
        
    return encodeList

print("Encoding ...")
encodingList = [encoding(imgList), studentId]
print("Encoding completed.")

# Save encoded file in pickle file
file = open('encodedFile.p', 'wb')
pickle.dump(encodingList, file)
file.close()
print("File created successfully.")
        