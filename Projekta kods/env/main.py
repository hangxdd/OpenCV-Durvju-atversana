import threading
import cv2
import time
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False
end_flag = False

reference_img=cv2.imread("reference.jpg")

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
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