import threading
import cv2
import time
import boto3
import numpy as np
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False
end_flag = False

s3 = boto3.client('s3', region_name='eu-north-1')
bucket_name = 'opencvimages'

def list_files(bucket_name, prefix='', visited=None):
    if visited is None:
        visited = set()

    if prefix in visited:
        return
    visited.add(prefix)

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith('/'):  # This is a folder
            yield from list_files(bucket_name, key, visited)  # Recursively list files in this folder
        else:  # This is a file
            yield key

reference_imgs = []
for file_key in list_files(bucket_name):

    # Get the file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)

    # Read the file's content into a numpy array
    arr = np.asarray(bytearray(obj['Body'].read()), dtype=np.uint8)

    # Decode the numpy array as an image
    reference_img = cv2.imdecode(arr, -1)

    reference_imgs.append(reference_img)

def check_face(frame):
    global face_match
    for reference_img in reference_imgs:
        try:
            if DeepFace.verify(frame, reference_img.copy())['verified']:
                face_match = True
                break
        except ValueError:
            pass
    if not face_match:
        face_match = False

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
    print("Face found! Door's opening.")
else:
    print("No matching face found...")

cap.release()
cv2.destroyAllWindows()