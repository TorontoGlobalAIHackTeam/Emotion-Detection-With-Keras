import cv2;
import numpy as np;
import os;
from pathlib import Path
import emotion_prediction as e_p

def main():

    curr_path = os.path.dirname(os.path.realpath(__file__));


    directory_in_str = str(curr_path) + "/Input";
    output_directory = str(curr_path) + "/Output";

    all_faces = [];

    pathlist = Path(directory_in_str)
    for path in pathlist.iterdir():
        # because path is object not string
        path_in_str = str(path)
        # print(path_in_str)

        #image path
        #imagePath = input("Image path: ");
        imagePath = path_in_str;

        #hardcoded cascPath
        #cascPath = "C:/Users/Owner/Desktop/AI Hackathon/Haar_Cascades/haarcascade_frontalface_default.xml"
        cascPath = str(curr_path) + "/Haar_Cascades/haarcascade_frontalface_default.xml"

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

            face_resize = cv2.resize(blank_image, (48, 48), 3);

            all_faces.append(face_resize);


    colour_list = [];

    out_arr = []

    output_file = open(output_directory + "/output_file.txt", "w");
    for i in range(0, len(all_faces)):

        file_string = "[";

        file_arr = []

        for j in range(0, 48):

            row = []

            file_string += "["
            for k in range(0, 48):
                file_string += str(all_faces[i][j][k][0]);
                row.append(all_faces[i][j][k][0])

                if (k != 47):
                    file_string += ","


            file_arr.append(row)



            file_string += "],"

        file_string = file_string.strip(",");
        out_arr.append(file_arr)



        output_file.write(file_string + "]\n");

        cv2.imwrite(output_directory + "/face_" + str(i) + ".jpg", all_faces[i]);


    if (len(out_arr) > 0):

        print (e_p.emotion(out_arr[0]))
        return e_p.emotion(out_arr[0])


    output_file.close()
    #cv2.waitKey(0);
main()
