import threading
import cv2
import time
import numpy as np
from deepface import DeepFace
from firebase_admin import credentials, initialize_app, storage
import io

# Import Django settings
import os
import sys
import django

# Add the User_control_system_website directory to the Python path
sys.path.append('C:\\Users\\mrliv\\Documents\\Skolas Lietas\\Prakse (4. kurss)\\Elektromagnētisko durvju atvēršana ar sejas atpazīšanu projekts\\Testa projekta kods\\User_control_system_website')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'usercontrolweb.settings')

# Set up Django
django.setup()

# Import the User model
from myapp.models import User


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False
end_flag = False

# Initialize Firebase
cred = credentials.Certificate(r"C:\Users\mrliv\Documents\Skolas Lietas\Prakse (4. kurss)\opencvimages-68d985d98e03.json")
initialize_app(cred, {'storageBucket': 'opencvimages.appspot.com'})

bucket = storage.bucket()

def list_files():
    # List all files in the Firebase Storage bucket
    blobs = bucket.list_blobs()
    return blobs

reference_imgs = []
for blob in list_files():
    # Only process blobs that are images (i.e., their names end with .png, .jpg, or .jpeg)
    if blob.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Get the file from Firebase Storage
        blob_bytes = blob.download_as_bytes()

        # Convert the bytes to a numpy array
        nparr = np.frombuffer(blob_bytes, np.uint8)

        # Decode the numpy array as an image
        reference_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Extract the user identifier from the file path
        user_id = blob.name.split('/')[0]

        reference_imgs.append((reference_img, user_id))

def check_face(frame):
    global face_match
    for reference_img, user_id in reference_imgs:
        try:
            if DeepFace.verify(frame, reference_img.copy())['verified']:
                face_match = True
                return user_id
        except ValueError:
            pass
    if not face_match:
        face_match = False
    return None

def end_program():
    time.sleep(0.5)
    global end_flag
    end_flag = True

start_time = time.time()

while True:
    if time.time() - start_time > 10 or end_flag:  # 10 seconds have passed or end flag is set
        break

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) #Makes the camera not inverted
    
    if ret:
        remaining_time = 10 - int(time.time() - start_time)
        cv2.putText(frame, str(remaining_time), (550, 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            threading.Thread(target=end_program).start()
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow("Face recognition", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

if face_match:
    user_id = check_face(frame)
    user = User.objects.get(identifier=user_id)
    print(f"Face match!")
    print(f"Welcome {user.name} {user.surname}!")
    print(f"Door's opening...")
else:
    print("No matching face found...")

cap.release()
cv2.destroyAllWindows()