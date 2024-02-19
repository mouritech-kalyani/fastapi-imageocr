import pytesseract
import PIL.Image
import cv2

myConfig = r"--psm 11 --oem 3"

# text = pytesseract.image_to_string(PIL.Image.open('./signs.jpeg'), config=myConfig)
# print(text)

img = cv2.imread('./img.png')
height, width, _ = img.shape
boxes = pytesseract.image_to_boxes(img, config= myConfig)
for box in boxes.splitlines():
    box = box.split(' ')
    img = cv2.rectangle(img, (int(box[1]), height - int(box[2])), (int(box[3]), height - int(box[4])), (0,255,0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
