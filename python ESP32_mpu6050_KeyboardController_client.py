# 客戶端(電腦端)
import socket          # Socket是一種網路通訊的API
from pynput import keyboard
from pynput.keyboard import Key
import time

use_keyboard=keyboard.Controller()

sock=socket.socket()
sock.connect(('192.168.18.8',9999))

print('開始')

while True:
    data=sock.recv(1024)

    if(data==b"left"):
        use_keyboard.press(Key.left)
        use_keyboard.release(Key.left)
        print('left')

    elif(data==b"right"):
        use_keyboard.press(Key.right)
        use_keyboard.release(Key.right)
        print('right')

    elif(data==b"up"):
        use_keyboard.press(Key.up)
        use_keyboard.release(Key.up)
        print('up')

    elif(data==b"down"):
        use_keyboard.press(Key.down)
        use_keyboard.release(Key.down)
        print('down')
        
    elif(data==b"stop"):
        print('stop')
    
    elif(data==b"enter"):
        use_keyboard.press(Key.enter)
        use_keyboard.release(Key.enter)
        print('enter')
    
    data=''
    time.sleep(0.001)       # 稍微暫停一下
    
sock.close()                # 關閉 socket        

