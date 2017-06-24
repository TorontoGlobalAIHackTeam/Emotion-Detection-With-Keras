import cv2;
import numpy as np;
import os;
from pathlib import Path

curr_path = os.path.dirname(os.path.realpath(__file__));

#directory_in_str = input("Enter image directory path: ");
#output_directory = input("Enter Output directory path: ");

directory_in_str = str(curr_path) + "\\Input";
output_directory = str(curr_path) + "\\Output";

all_faces = [];

pathlist = Path(directory_in_str) #.glob('**/*.asm')
for path in pathlist.iterdir():
    # because path is object not string
    path_in_str = str(path)
    # print(path_in_str)

    #image path
    #imagePath = input("Image path: ");
    imagePath = path_in_str;

    #hardcoded cascPath
    #cascPath = "C:\\Users\\Owner\\Desktop\\AI Hackathon\\Haar_Cascades\\haarcascade_frontalface_default.xml"
    cascPath = str(curr_path) + "\\Haar_Cascades\\haarcascade_frontalface_default.xml"

    #create haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath);

    #Read image
    image = cv2.imread(imagePath) 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);

    #Detect faces in image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        flags = cv2.COLOR_BGR2HSV
    );

    print ("Found " + str(len(faces)) + " faces.");

    count = 0;

    for (x, y, w, h) in faces:

        w = max(w,h);
        h = max(w,h);

        count += 1;
        
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), 2);
        blank_image = np.zeros((h, w, 3), np.uint8);

        for i in range(0, w):
            for j in range(0, h):
                blank_image[j][i] = gray[y + j][x + i];

        #cv2.imshow("Face " + str(count), blank_image);

        all_faces.append(blank_image);

for i in range(0, len(all_faces)):
    #cv2.imshow("Face " + str(i), all_faces[i]);
    cv2.imwrite(output_directory + "\\face_" + str(i) + ".jpg", all_faces[i]);

cv2.waitKey(0);
