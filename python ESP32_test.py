from machine import Pin
import time

# 建立2號腳位的Pin物件,設定腳位輸出.
led=Pin(2,Pin.OUT)

while True:
    led.value(1)     # 點亮LED
    time.sleep(0.5)
    led.value(0)     # 關閉LED
    time.sleep(0.5)

