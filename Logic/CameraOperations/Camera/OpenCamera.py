import cv2
from time import sleep
from Logic.SaveFile.SaveFile import *
import asyncio


async def open_camera(path):
    count = 0
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while webcam.isOpened():
        try:
            count = 1
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                count += 1
                await save_image(image=frame, image_name=f"saved_image{count}.jpg", path=path)

            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break

        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("CameraOperations off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
