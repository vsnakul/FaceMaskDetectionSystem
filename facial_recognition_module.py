import face_recognition
import os
import cv2

import numpy as np


#KNOWN_FACES_DIR = 'known_faces'
#UNKNOWN_FACES_DIR = 'unknown_faces'
#TOLERANCE = 0.47
#FRAME_THICKNESS = 3
#FONT_THICKNESS = 2
#MODEL = 'hog'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model
# Returns (R, G, B) from name
class FacialIdentificationSystem(object):
    def __init__(self):
        KNOWN_FACES_DIR = 'known_faces'
        # UNKNOWN_FACES_DIR = 'unknown_faces'
        self. TOLERANCE = 0.47
        self.FRAME_THICKNESS = 3
        self.FONT_THICKNESS = 2
        self.MODEL = 'hog'
        self.video = cv2.VideoCapture(0)
        print('Loading known faces...')
        self.known_faces = []
        self.known_names = []
        # We oranize known faces as subfolders of KNOWN_FACES_DIR
        # Each subfolder's name becomes our label (name)
        for name in os.listdir(KNOWN_FACES_DIR):

            # Next we load every file of faces of known person
            for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):

                image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
                encoding = face_recognition.face_encodings(image)
                if len(encoding) > 0:
                    encoding = encoding[0]
                else:
                    print("No faces found in the image...")
                    break

                # Append encodings and name
                self.known_faces.append(encoding)
                self.known_names.append(name)

    print('Processing unknown faces...')
    # Now let's loop over a folder of faces we want to label
    def generate_frames_to_show(self):

        while True:
            ret,image=self.video.read()
            print("inside generate ")
            locations = face_recognition.face_locations(image,number_of_times_to_upsample=0,model='hog')
            encodings = face_recognition.face_encodings(image, locations)
            print(f', found {len(encodings)} face(s)')
            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(self.known_faces, face_encoding, self.TOLERANCE)
                match = None
                if True in results:  # If at least one is true, get a name of first of found labels
                    match = self.known_names[results.index(True)]
                    print(f' - {match} from {results}')

                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])

                    cv2.rectangle(image, top_left, bottom_right, [0,255,0], self.FRAME_THICKNESS)

                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)

                    cv2.rectangle(image, top_left, bottom_right, [0,255,0], cv2.FILLED)

                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), self.FONT_THICKNESS)

            # Show image
            #cv2.imshow(filename, image)
            ret,jpeg=cv2.imencode('.jpg',image)
            #print("here is the data in bytes ",frames)
            return jpeg.tobytes()

       # if cv2.waitKey(1) & 0xFF==ord("q"):
      #      break
    #cv2.waitKey(0)
    #cv2.destroyWindow(filename)
