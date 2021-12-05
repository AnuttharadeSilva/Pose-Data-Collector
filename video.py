import mediapipe as mp
import cv2
import csv
import numpy as np
import time
import uuid
import os
import shutil


class Video:
    def collect_data(self, file_name, class_name):
        mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
        mp_holistic = mp.solutions.holistic  # Mediapipe Solutions

        csv_file_path = 'datasets/'+file_name+'.csv'

        num_coords = 533  # (468+21+21+23)
        num_coords_pose = 23
        landmarks = ['class', 'image']
        for val in range(1, num_coords_pose+1):
            landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val), 'v{}'.format(val)]
        for val in range(num_coords_pose+1, num_coords+1):
            landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val)]

        with open(csv_file_path, mode='w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(landmarks)

        image_path = 'datasets/'+file_name
        if not os.path.exists(image_path):
            os.mkdir(image_path)

        class_name = class_name

        cap = cv2.VideoCapture(0)
        timeout = time.time() + 30
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                ret, frame = cap.read()

                # Recolor Feed
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make Detections
                results = holistic.process(image)

                # Recolor image back to BGR for rendering
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 1. Draw face landmarks
                mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                         mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                         mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                         )

                # 2. Right hand
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                          )

                # 3. Left Hand
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                          )

                # 4. Pose Detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                # Export coordinates
                try:
                    # Extract Pose landmarks
                    if (results.pose_landmarks != None):
                        pose = results.pose_landmarks.landmark[:23]
                        pose_row = list(
                            np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                    else:
                        pose_row = [0] * 23 * 4

                    # Extract left hand landmarks
                    if (results.left_hand_landmarks != None):
                        left_hand = results.left_hand_landmarks.landmark
                        left_hand_row = list(np.array(
                            [[landmark.x, landmark.y, landmark.z] for landmark in left_hand]).flatten())
                    else:
                        left_hand_row = [0] * 21 * 3

                    # Extract right hand landmarks
                    if (results.right_hand_landmarks != None):
                        right_hand = results.right_hand_landmarks.landmark
                        right_hand_row = list(np.array(
                            [[landmark.x, landmark.y, landmark.z] for landmark in right_hand]).flatten())
                    else:
                        right_hand_row = [0] * 21 * 3

                    if (results.face_landmarks != None):
                        face = results.face_landmarks.landmark
                        face_row = list(
                            np.array([[landmark.x, landmark.y, landmark.z] for landmark in face]).flatten())
                    else:
                        face_row = [0] * 468 * 3

                    # Concate rows
                    row = pose_row + left_hand_row + right_hand_row + face_row

                    # Append class name
                    row.insert(0, class_name)

                    image_name = '{}.jpg'.format(uuid.uuid1())
                    cv2.imwrite(os.path.join(image_path, image_name), frame)

                    row.insert(1, image_name)

                    # Export to CSV
                    with open(csv_file_path, mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(row)

                except:
                    pass

                window_name = 'Webcam Feed'
                cv2.namedWindow(window_name)
                cv2.moveWindow(window_name, 40, 10)
                cv2.imshow(window_name, image)
                cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

                if time.time() > timeout:
                    break

        shutil.make_archive(image_path, 'zip', image_path)
        # os.rmdir(image_path)
        # shutil.rmtree(image_path, ignore_errors=True)

        cap.release()
        cv2.destroyAllWindows()

