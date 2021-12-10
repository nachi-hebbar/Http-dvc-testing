import os
import cv2
import json
path="data_copy/"
files=os.listdir(path)
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  
for file in files:
    file_path=path+file
    print(file_path)
    if file_path[-3:]=="png":
        image_file=file_path
        json_file=file_path[:-3]+"json"
        #image_file=json_file[:-4]+"jpg"
        print("Current image", image_file)
        image=cv2.imread(image_file)
        f=open(json_file)
        json_read=json.load(f)
        shapes=json_read["shapes"]
        for object in shapes:
            #print(object["points"][1])
            xmin,ymin,xmax,ymax=object["points"][0][0],object["points"][0][1],object["points"][1][0],object["points"][1][1]
            xmin,ymin,xmax,ymax=int(abs(xmin)),int(abs(ymin)),int(abs(xmax)),int(abs(ymax))
            print("XMin: {} Ymin: {}".format(xmin,ymin))
            print("Xmax : {} Ymax: {}".format(xmax,ymax))
            if object["label"]=="triple_riding": 
            	image=cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,0,255),3)
            if object["label"]=="no_triple_riding":
                image=cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(255,0,0),2)
            if object["label"]=="bike":
                image=cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,255,0),2)
        cv2.imshow("Image",image)
        cv2.waitKey()
