# import-Module psreadlines
# import psreadlines
import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
im = cv2.imread("C:\\Users\\Mshinz\\Desktop\\cc++\\python.py\\python\\haarcascades\\cars.jpg")
im = imutils.resize(im, width=300)
cv2.imshow("original imaged", im)
cv2.waitKey(0)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cv2.imshow("1 - Grayscale Conversion", gray)
cv2.waitKey(0)

gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("2 - Bilateral Filter", gray)
cv2.waitKey(0)

edged = cv2.Canny(gray, 30, 200)
cv2.imshow("4 - Canny Edges", edged)
cv2.waitKey(0)

cnts,new= cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
imag =im.copy()
cv2.drawContours(imag, cnts, -1,(0,255,0),3)
cv2.imshow("conturs", imag)
cv2.waitKey(0)


cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
screebCnt = None
imag1 = im.copy()
cv2.drawContours(imag1, cnts,-1,(0,255,0),3)
cv2.imshow("top 30 con",imag1)
cv2.waitKey(0)


i=7
for c in cnts:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.0018*perimeter,True)
    if len(approx)==4:
        screebCnt= approx
    break
# Larg= 0
# for c in cnts:
#     x,y,w,h = cv2.boundingRect(c)
#     area = 4*w*h
#     if area > Larg:
#         Larg = area
#         larg_area_contour = c

x,y,w,h = cv2.boundingRect(c)
cv2.rectangle(im, (x,y),(x+w, y+h),(36,255,12),2)
cv2.imshow("myt",im)
new_im =im[y:y+h, x:x+w]
cv2.imwrite('./'+str(i)+'.png',new_im)
i+=1
        # break

# cv2.drawContours(im, [screebCnt], -1, (0,255,0), 3)
# cv2.imshow("ijhg", im)
# cv2.waitKey(0)


cropped_loc = './7.png'
cv2.imshow("cropped", cv2.imread(cropped_loc))
plate = pytesseract.image_to_string(cropped_loc, lang='eng')
print("Number palate is:", plate)
cv2.waitKey(0)
cv2.destroyAllWindows()

#  NumberPlateCnt = None #we currently have no Number plate contour

# count = 0
# for c in cnts:
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#         if len(approx) == 4:  # Select the contour with 4 corners
#             NumberPlateCnt = approx #This is our approx Number Plate Contour
#             break

# cv2.drawContours(im, [NumberPlateCnt], -1, (0,255,0), 3)
# cv2.imshow("Final Image With Number Plate Detected", im)



