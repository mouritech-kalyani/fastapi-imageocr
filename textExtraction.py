import pytesseract
from PIL import Image

img_path = "./cycle.jpg"

models_checkpoints = {
    "LayoutLMv1 for Invoices" : "impira/layoutlm-document-qa",
    "Donut": "naver-clova-ix/donut-base-finetuned-docvqa",
}
image = Image.open(img_path)
text = pytesseract.image_to_string(image)
# print(text)
if 'income tax department' in text.lower() or 'permanent account number' in text.lower():
    print('This is PAN Card')
elif 'driving licence' in text.lower() or 'valid till' in text.lower():
    print("This is Driving Licence")
elif 'republic of india' in text.lower() or 'date of expiry' in  text.lower():
    print('This is Passport')
elif 'government of India' in text.lower() or 'male' in text.lower() or 'female' in text.lower():
    print('This is adhar card')    
else:
    print('Please upload valid document')
        

       
# from transformers import pipeline
# pipe = pipeline("document-question-answering", model="impira/layoutlm-document-qa")
# nameOfPerson = pipe(image=img_path, question = "What is the name of the person?")
# print('Name : ',nameOfPerson[0]['answer'])
# dob = pipe(image=img_path, question = "What is DOB of the person?")
# print('DOB : ', dob[0]['answer'])
# gender = pipe(image=img_path, question = "What is gender of the person?")
# print("Gender : ", gender[0]['answer'])
# adharNo = pipe(image=img_path, question = "What is adhar number of the person?")
# print("Adhar Number : ", adharNo[0]['answer'])
