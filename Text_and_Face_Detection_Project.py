""" Take a ZIP file of images and process them, using a library built into python that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images. Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new (library), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets. """
#hint 2
import zipfile
import PIL
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

def extract_zipfile(zipfile_name):
    lst_images = {}   
    myzip = zipfile.ZipFile(zipfile_name) 
    for entry in myzip.infolist():
        file = myzip.open(entry)
        lst_images[file.name] = [Image.open(file), file]
       
    return lst_images

def text_and_face_detection(image):
    
    output_image = image.convert("L")
    text = pytesseract.image_to_string(output_image)
    if "Christopher" in text:
         #lst_images[file.name].save("msi_recruitment.png")
        mg = cv.imread("msi_recruitment.png")
        gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE1)
        return faces
    else:
        pass

def crop_faces(faces, file_name):
    list_faces = []
    image = Image.open(file_name).convert("RGB")
    for x,y,w,h in faces:
        list_faces.append(image.crop((x,y,x+w,y+h)))
    
    return list_faces

def contact_sheet(images):
    # creating a nine image square (3 by 3)
    first_image = images[0]
                
    contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*5, first_image.height*2), )
    x=0
    y=0

    for img in images:
        # Lets paste the current image into the contact sheet
        contact_sheet.paste(img, (x, y) )    
        # Now we update our X position. If it is going to be the width of the image, then we set it to 0
        # and update Y as well to point to the next "line" of the contact sheet.
        if x + first_image.width == contact_sheet.width:
            x = 0
            y = y + first_image.height
        else:
            x = x + first_image.width
    return contact_sheet
    


    #ret, thresh = cv2.threshold(lst_images[file.name], 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = 128
    # images of different threshold values
    #for thresh in range(0,257,64):
       # print("Trying with threshold " + str(thresh))
smalll_img_zip = 'readonly/small_img.zip'
list_small_img = extract_zipfile(smalll_img_zip)
list_images_zip = 'readonly/images.zip'

for small_img in list_small_img:
    g = small_img.key()
    crop_faces(text_and_face_detection(small_img[g][0]), small_img[g][0])
    
        #cv_img_bin = cv.threshold(lst_images[file.name],120,255,cv.THRESH_BINARY)[1]
        # Now do the actual face detection
       
        #print('Results found in file {}'.format(file.name))
       # contact_sheet(list_faces)
