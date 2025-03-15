import cv2
import face_recognition as fr
import pickle
import os
from firebase_setup import firebase_storage  # Import storage from Firebase setup

# Path to student images
IMG_PATH = 'Images'

def load_images(image_folder):
    """Loads images from the given folder and extracts student IDs."""
    img_list = []
    student_ids = []
    
    if not os.path.exists(image_folder):
        print(f"Error: Folder '{image_folder}' not found.")
        return img_list, student_ids

    for file in os.listdir(image_folder):
        file_path = os.path.join(image_folder, file)
        img = cv2.imread(file_path)

        if img is not None:
            img_list.append(img)
            student_ids.append(os.path.splitext(file)[0])  # Extract student ID from filename
        else:
            print(f"Warning: Unable to read image {file}")

    return img_list, student_ids

def upload_images_to_firebase(image_folder):
    """Uploads images to Firebase Storage."""
    try:
        bucket = firebase_storage.bucket()
        for file in os.listdir(image_folder):
            file_path = os.path.join(image_folder, file)
            blob = bucket.blob(f'{image_folder}/{file}')
            blob.upload_from_filename(file_path)
        print("Images uploaded to Firebase Storage.")
    except Exception as e:
        print(f"Error uploading images: {e}")

def encode_faces(images):
    """Encodes faces using face_recognition library."""
    encode_list = []
    
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        face_encodings = fr.face_encodings(img_rgb)

        if face_encodings:
            encode_list.append(face_encodings[0])  # Store first detected face encoding
        else:
            print("No face detected in an image.")
    
    return encode_list

def save_encodings_to_pickle(encodings, student_ids, output_file="encodedFile.p"):
    """Saves encodings and student IDs into a pickle file."""
    try:
        with open(output_file, 'wb') as file:
            pickle.dump([encodings, student_ids], file)
        print(f"Encodings saved to {output_file}.")
    except Exception as e:
        print(f"Error saving encodings: {e}")

def main():
    """Main function to process images, encode faces, and upload data."""
    print("Loading images...")
    img_list, student_ids = load_images(IMG_PATH)

    if not img_list:
        print("No valid images found. Exiting.")
        return

    print("Uploading images to Firebase Storage...")
    upload_images_to_firebase(IMG_PATH)

    print("Encoding faces...")
    encodings = encode_faces(img_list)
    print("Encoding completed.")

    print("Saving encoded data...")
    save_encodings_to_pickle(encodings, student_ids)

if __name__ == "__main__":
    main()