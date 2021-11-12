import msgpack, msgpack_numpy as m, cv2, numpy as np, elara
from func import *
from requests import post
from Bot import uid, API_TOKEN

# variables
video_capture = cv2.VideoCapture(2)
face_locations = []
face_encodings = []
face_names = []


while True:
    # a frame of video
    ret, frame = video_capture.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    # resize frame
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # from BGR to RGB
    rgb_small_frame = small_frame[:, :, ::-1]
    # all the faces and face encodings a frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    db = elara.exe("encodings.db", True)
    arr = msgpack.unpackb(db.get("seen encodings"), object_hook=m.decode)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # is face in seen encodings
        if True not in face_recognition.compare_faces(arr, face_encoding):
            # if the face is in the known
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            # normalizing face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # cropping frame to get the face
            face = frame[top:bottom, left:right]
            cv2.imwrite(f'./todo/{name}.jpeg', face)
            post(f'''https://api.telegram.org/bot{API_TOKEN}/sendPhoto?chat_id={uid}&caption=Виявлено нового порушника!
Ім'я: {name}''', files={'photo': open(f"./todo/{name}.jpeg", 'rb')})
            os.remove(f"./todo/{name}.jpeg")
            arr.append(face_encoding)
            db.set("seen encodings", msgpack.packb(arr, default=m.encode))
