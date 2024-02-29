from io import BytesIO
import os
import cv2
from fastapi import FastAPI, File, UploadFile
from transformers import pipeline
import pytesseract
from PIL import Image
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# pytesseract.pytesseract.tesseract_cmd =  '/Library/Frameworks/Python.framework/Versions/3.10/bin/pytesseract'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# UPLOADS_DIR = 'uploads'
# os.makedirs(UPLOADS_DIR, exist_ok=True)


@app.get('/')
async def root():
    return{'example' : 'This is eg', 'data': 0}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    print('file', file.filename)
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
    # Convert bytes to a PIL Image
    image = Image.open(file.filename)
    text = pytesseract.image_to_string(image, lang = 'eng')
    
    # image = Image.open(BytesIO(await file.read()))

    # Use pytesseract to extract text from the image
    # text = pytesseract.image_to_string(image)
    
    finalAns = []
    # Load the image for processing
    if 'income tax department' in text.lower() or 'permanent account number' in text.lower():
       fileType = 'PAN Card'
    elif 'driving licence' in text.lower() or 'valid till' in text.lower():
        fileType = 'Driving Licence'
    elif 'republic of india' in text.lower() or 'date of expiry' in  text.lower():
        fileType = 'Passport'
    elif 'government of India' in text.lower() or 'male' in text.lower() or 'female' in text.lower():
        fileType = 'Adhar Card'
    else:
        fileType = 'Please Upload valid document'
    print('text is --',len(text), fileType)
    # To check image is blur or not
    isBlurry = False
    if len(text) > 0:
        isBlurry = is_image_blurry(file.filename)

    if isBlurry:
        print("The uploaded image is blurry.")
    else:
        print("The uploaded image is not blurry.")
    pipe = pipeline("document-question-answering", model="impira/layoutlm-document-qa")

    if fileType == 'Adhar Card' and len(text) > 0:
        nameOfPerson = pipe(image=file.filename, question = "What is the name of the person?")
        dob = pipe(image=file.filename, question = "What is DOB of the person?")
        gender = pipe(image=file.filename, question = "What is gender of the person?")
        aadhar_number_match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', text)
        if aadhar_number_match:
            adharNumber =  aadhar_number_match.group(0).replace(' ', '')  # Remove spaces
        else:
            adharNumber = 'Not Found'
        
        
        finalAns.append(
            {
                'Name': nameOfPerson[0]['answer'],
                'DOB': dob[0]['answer'],
                'Gender': gender[0]['answer'],
                'AdharNumber': adharNumber,
            }
        )
    elif fileType == 'PAN Card'  and len(text) > 0:  
        nameOfPerson = pipe(image=file.filename, question = "What is the name of the person?")
        fathersName = pipe(image=file.filename, question = "What is the father's name or mother's name?")
        dob = pipe(image=file.filename, question = "What is Date of birth?")
        panNoMatches = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
        if panNoMatches:
            panNumber =  panNoMatches.group(0).replace(' ', '')  # Remove spaces
        else:
            panNumber = 'Not Found'
        
        finalAns.append(
            {
                'Name': nameOfPerson[0]['answer'],
                'fathersName': fathersName[0]['answer'],
                'DOB': dob[0]['answer'],
                'PanCardNumber': panNumber,
            }
        )
    elif fileType == 'Passport' and len(text) > 0:  
        
        surname =  pipe(image=file.filename, question = "What is the Surname of the person ?")
        nameOfPerson = pipe(image=file.filename, question = "What is the Given name of the person ?")
        dob = pipe(image=file.filename, question = "What is Date of Birth of the person?")
        # gender = pipe(image=file.filename, question = "What is the gender M or F ?")
        passportNumber = pipe(image=file.filename, question = "What is passport number of the person?")
        nationality = pipe(image=file.filename, question = "What is nationality?")
        placeOfBirth = pipe(image=file.filename, question = "What is Place of the birth in this passport ?")
        placeOfIssue = pipe(image=file.filename, question = "what is Place of Issue where this passport has been issued ?")
        dateOfIssue = pipe(image=file.filename, question = "what is Date of Issue mentioned in this passport?")
        dateOfExpiry = pipe(image=file.filename, question = "what is Date of expiry?")
        sex_patterns = [
        r'Sex (M|F|Other)',
        r'Sex (Male|Female|Other)',
        r'(?<=Sex)(.*?)(?=<<)',  # In case "Sex:" is followed by other details
        r'(?<=SEX)(.*?)(?=<<)',  # In case "SEX:" is followed by other details
        r'(?<=Sex)(.*?)(?=<<)',   # In case "Sex" is followed by other details
        r'(?<=SEX)(.*?)(?=<<)'    # In case "SEX" is followed by other details
    ]
        gender = None
        for pattern in sex_patterns:
            match = re.search(pattern, text)
            if match:
                gender = match.group(1)
            else:
                gender = 'Not Found'
        
        finalAns.append(
            {
                'Name': nameOfPerson[0]['answer'],
                'Surname': surname[0]['answer'],
                'DOB': dob[0]['answer'],
                'Gender': gender,
                'PassportNumber': passportNumber[0]['answer'],
                'Nationality': nationality[0]['answer'],
                'PlaceOfBirth': placeOfBirth[0]['answer'],
                'PlaceOfIssue': placeOfIssue[0]['answer'],
                'DateOfIssue': dateOfIssue[0]['answer'],
                'DateOfExpiry': dateOfExpiry[0]['answer']
            }
        )             
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    if(isBlurry):
        return {"isBlurry": isBlurry}
    return [{"filename": file.filename, "fileType": fileType, "Answer": finalAns, "isBlurry": isBlurry}]    
    

def is_image_blurry(image_path, threshold=0.6):
    # Read the image
    imageIS = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(imageIS, cv2.COLOR_BGR2GRAY)
    # Perform OCR using Tesseract
    ocr_text = pytesseract.image_to_string(imageIS)
    # Check OCR output for clarity
    words = ocr_text.split()
    clear_word_count = 0
    total_word_count = len(words)
    
    for word in words:
        # Measure word clarity based on length or other criteria
        if len(word) >= 3:  # Adjust this condition based on your requirements
            clear_word_count += 1
    
    clarity_ratio = clear_word_count / total_word_count
    
    # Determine if the image is blurry based on clarity ratio
    if clarity_ratio < threshold:
        return True
    else:
        return False