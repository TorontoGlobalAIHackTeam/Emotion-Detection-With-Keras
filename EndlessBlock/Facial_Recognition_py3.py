import cv2;
import numpy as np;
import os;
from pathlib import Path

curr_path = os.path.dirname(os.path.realpath(__file__));

output_directory = str(curr_path) + "\\Output";

faceGlobal = [];

def cropPic(image):
  #hardcoded cascPath
  #cascPath = "C:\\Users\\Owner\\Desktop\\AI Hackathon\\Haar_Cascades\\haarcascade_frontalface_default.xml"
  cascPath = str(curr_path) + "\\Haar_Cascades\\haarcascade_frontalface_default.xml"

  #create haar cascade
  faceCascade = cv2.CascadeClassifier(cascPath);

  #gray image
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);

  #Detect faces in image
  face = faceCascade.detectMultiScale(
      gray,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(30, 30),
      #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
      flags = cv2.COLOR_BGR2HSV
  );

  print ("Found the face");

  count = 0;

  for (x, y, w, h) in face:

      w = max(w,h);
      h = max(w,h);

      count += 1;
      
      cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), 2);
      blank_image = np.zeros((h, w, 3), np.uint8);

      for i in range(0, w):
          for j in range(0, h):
              blank_image[j][i] = gray[y + j][x + i];
              
      face_resize = cv2.resize(blank_image, (48, 48), 3);

      faceGlobal = face_resize;


  colour_list = [];

  output_file = open(output_directory + "\\output_file.txt", "w");
  file_string = "";

  global faceGlobal
  file_string += str(faceGlobal);

  file_string = file_string.strip();

  output_file.write(file_string + "\n");
  
  cv2.imwrite(output_directory + "\\face.jpg", faceGlobal[0]);

  cv2.waitKey(0);

def main():
  cropPic(image)
  
if __name__ == "__main__":
   main()
