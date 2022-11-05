import utils
import time
import cv2
import os

URL = '' # copy and paste your Theos deployment URL here
FOLDER_PATH = 'guns'

seconds_to_wait = 2

if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)

camera = cv2.VideoCapture(0)

if camera.isOpened():
    camera_open, frame = camera.read()
else:
    camera_open = False

start = time.time()
print('[+] starting gun detection...')

while camera_open:
    recording, frame = camera.read()
    elapsed = time.time() - start

    if elapsed >= seconds_to_wait:
        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        now = utils.get_time()

        try:
          detections = utils.detect(image_bytes, url=URL)
          if len(detections) > 0:
            detected_frame = utils.draw(frame, detections)
            utils.save_frame(detected_frame, os.path.join(FOLDER_PATH, now + '.jpg'))
            print(f'[{now}] [!] gun detected')
        except Exception as error:
          pass

        start = time.time()

camera.release()