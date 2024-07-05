import cv2
import glob
import os
from emailing import send_email
video = cv2.VideoCapture(0)
first_frame= None
status_list=[]
count=1
def clean_folder():
    images=glob.glob("images/*.png")
    for image in images:
        os.remove(image)
while True:
    status=0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  ##conveting the Frame into grayscale frame to reduce the amount of data by applying the algorithum
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21),0) #ksize indicate the amount of Blurness

    ## making the difference of preprocess frames
    if first_frame is None:
        first_frame=gray_frame_gau
    delta_frame = cv2.absdiff(first_frame ,gray_frame_gau)
    thresh_frame=cv2.threshold(delta_frame,65,255,cv2.THRESH_BINARY)[1] ## reassign the value of 30 -> 255 by applying the Thresh_binary algo
    dil_frame=cv2.dilate(thresh_frame,None,iterations=2)  ## To remove the noise

    contours,check= cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour)<5000:  ##if counter is less than 5000 we assume there is no object
            continue
        x,y,w,h = cv2.boundingRect(contour)  #we are extrating the x and y and w and h
        rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        if rectangle.any():
            status=1
            cv2.imwrite(f"images/{count}.jpg", frame)
            count += 1
            all_images=glob.glob("images/*.jpg") ## glob appending all the name of images into a list
            index_of_final_image = len(all_images)//2
            image_with_object=all_images[index_of_final_image]
            print(image_with_object)

    status_list.append(status)
    status_list=status_list[-2:]
    print(status_list)

    if status_list[0]==1 and status_list[1]==0:
        send_email(image_with_object)
        ##clean_folder()
        break
    cv2.imshow("my video", frame)
    key = cv2.waitKey(1)   ##create a keyboard key object
    if key == ord("q"):
        break

video.release()


