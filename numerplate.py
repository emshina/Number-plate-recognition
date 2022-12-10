from tkinter import*
from PIL import ImageTk,Image
from tkinter import filedialog
import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
import unicodedata

root=Tk()
root.title("NUMBER PLATE DETECTION SYSTEM")
root.geometry("900x600")
root.config(bg="black",highlightthickness=7,highlightcolor="blue")


# canva = Canvas(root, bd=2,highlightthickness=2,)
# canva.pack(side=TOP, padx=10,pady=10)
lbtitle =Label(root, bd= 20, relief=RIDGE, text="NUMBERPLATE RECOGNITION SYSTEM", fg= "blue", bg="black", font=("times new roman",30))
lbtitle.pack(side=TOP, fill=X)
global img
def open():
    global img
    root.filename = filedialog.askopenfilename(initialdir="/gui/images",title="selecet car"
                                            ,filetypes=(("jpg files","*.jpg"),("all files", "*.*")))
    img = cv2.imread(root.filename,cv2.IMREAD_COLOR)
    root.geometry("1540x800+0+0")
 

my_button = Button(root,bg="black", text="Open picture",bd=5,fg="blue",width=20, command=open)
my_button.place(x=0,y=95)

def process():

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise

    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
    cv2.imshow('image',edged)
    # cv2.imshow('image',img)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)

    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

    screenCnt = None


    # loop over our contours

    for c in cnts:

     # approximate the contour

     peri = cv2.arcLength(c, True)

     approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    

     # if our approximated contour has four points, then

     # we can assume that we have found our screen

     if len(approx) == 4:

        screenCnt = approx

        break
    if screenCnt is None:

     detected = 0

     print("No contour detected")

    else:

     detected = 1


    if detected == 1:

     cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)


    # Masking the part other than the number plate

    mask = np.zeros(gray.shape,np.uint8)

    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)

    new_image = cv2.bitwise_and(img,img,mask=mask)


    # Now crop

    (x, y) = np.where(mask == 255)

    (topx, topy) = (np.min(x), np.min(y))

    (bottomx, bottomy) = (np.max(x), np.max(y))

    Cropped = gray[topx:bottomx+1, topy:bottomy+1]
    
    #Read the number plate

    text = pytesseract.image_to_string(Cropped, config='--psm 11')

    print("Detected Number is:",text)


    cv2.imshow('image',img)

    cv2.imshow('Cropped',Cropped)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


my_button = Button(root,bd=5, text="Run",width=20,bg="black",fg="blue", command=process)
my_button.place(x=0,y=130)



root.mainloop()
