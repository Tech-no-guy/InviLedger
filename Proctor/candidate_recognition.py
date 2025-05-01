import cv2
import face_recognition
import os

def load_known_faces(folder):
    encodings = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder, filename)
            image = face_recognition.load_image_file(image_path)
            face_encs = face_recognition.face_encodings(image)
            if face_encs:
                encodings.append(face_encs[0])
    return encodings

known_face_encodings = load_known_faces("authorized_faces")

video_capture = cv2.VideoCapture(0)
unauthorized_flagged = False

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        if not any(matches) and not unauthorized_flagged:
            print("Unauthorized person detected! Screenshot saved.")
            cv2.imwrite("unauthorized_screenshot.jpg", frame)
            unauthorized_flagged = True
        if any(matches):
            print(" Authorized person detected.")

    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
