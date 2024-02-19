from transformers import pipeline
import tkinter as tk
from tkinter import Entry, Label, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
my_w = tk.Tk()
my_w.geometry("800x800")  # Size of the window 
my_w.title('www.ocr.com')
my_font1=('times', 18, 'bold')
l1 = tk.Label(my_w,text='Select ID Proof',width=30,font=my_font1)  
l1.grid(row=1,column=1)
b1 = tk.Button(my_w, text='Upload File', 
   width=20,command = lambda:upload_file())
b1.grid(row=2,column=1) 

img_path = "./dummyAadhar.jpeg"

models_checkpoints = {
    "LayoutLMv1 for Invoices" : "impira/layoutlm-document-qa",
    "Donut": "naver-clova-ix/donut-base-finetuned-docvqa",
}

filename = ''
def upload_file():
   global img
   f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'), ('Png Files', '*.png')]
   filename = filedialog.askopenfilename(filetypes=f_types)
   img=Image.open(filename)
   img_resized=img.resize((400,200)) # new width & height
   img=ImageTk.PhotoImage(img_resized)
   b2 =tk.Button(my_w,image=img) # using Button 
   b2.grid(row=3,column=1)
   pipe = pipeline("document-question-answering", model="impira/layoutlm-document-qa")
   nameOfPerson = pipe(image=filename, question = "What is the name of the person?")
   dob = pipe(image=filename, question = "What is DOB of the person?")
   gender = pipe(image=filename, question = "What is gender of the person?")
   adharNo = pipe(image=filename, question = "What is adhar number of the person?")
   labl_1 = Label(my_w, text="Full Name",width=20,font=("bold", 20))  
   labl_1.place(x=30,y=300)  
   labl_11 = Label(my_w, text=nameOfPerson[0]['answer'],width=20,font=("bold", 23))  
   labl_11.place(x=220,y=300) 
   
   labl_2 = Label(my_w, text="DOB",width=20,font=("bold", 20))  
   labl_2.place(x=30,y=350) 
   labl_22 = Label(my_w, text=dob[0]['answer'],width=20,font=("bold", 25))  
   labl_22.place(x=220,y=350) 
   
   labl_3 = Label(my_w, text="Gender",width=20,font=("bold", 20))  
   labl_3.place(x=30,y=400) 
   labl_33 = Label(my_w, text=gender[0]['answer'],width=20,font=("bold", 25))  
   labl_33.place(x=220,y=400)  

   labl_4 = Label(my_w, text="Adhar Number",width=20,font=("bold", 20))  
   labl_4.place(x=30,y=450) 
   labl_44 = Label(my_w, text=adharNo[0]['answer'],width=20,font=("bold", 25))  
   labl_44.place(x=240,y=450)  


   
 

my_w.mainloop()  # Keep the window open