#define BLYNK_TEMPLATE_ID "TMPL6cjI6_lEp"
#define BLYNK_TEMPLATE_NAME "Quickstart Template"
#define BLYNK_AUTH_TOKEN "99XXRoC73NaXkPY5v6lmPgvvFxpYA45-"

from machine import Pin,ADC       
import time
from keras_lite import Model   
import ulab as np
import BlynkLib
import network
import _thread

Blynk_AUTH = "99XXRoC73NaXkPY5v6lmPgvvFxpYA45"

#增加神經網路的參數
mean=248.36183333333332
std=588.2433993134969
model = Model('voice_model.json')   # 建立模型物件
label_name = ['on','off','others']  # label名稱

led=Pin(32,Pin.OUT,value=0)

adc=ADC(Pin(36))
adc.width(ADC.WIDTH_12BIT)     # 解析度12BT
adc.atten(ADC.ATTN_11DB)       # 最大電壓3.6V

#連線至基地台
sta=network.WLAN(network.STA_IF)
sta.active(True)   
sta.connect('a347','34716385')   
while not sta.isconnected():
    pass

print("連線至Blynk...")
blynk = BlynkLib.Blynk(Blynk_AUTH)
print("連線成功")

#啟用Blynk函式
def v3_handler(value):        # 讀取Blynk按鈕值
    led_status=int(value[0])  # Blynk所收到的值
    led.value(led_status)     # 更改燈號
    
blynk.on("V3",v3_handler)

def blynk_Thread():
    while True:
        blynk.run()

_thread.start_new_thread(blynk_Thread, ())

while True:
    sound=adc.read()       # 接收聲音資訊
    if(sound>2500):         # ADC>2500才紀錄,避免環境音誤觸
        print('')
        no_sound=0
        data=[sound]
        # 連續沒聲音次數少於150次且沒超過資料儲存量
        while(no_sound<150 and len(data)<400):
            sound=adc.read()
            data.append(sound)
            if(sound==0):
                no_sound+=1
            else:
                no_sound=0
            time.sleep_us(500)
        
        if(len(data)<150):
            print('noise,try again')
            continue
        
        while(len(data)<400):  # 資料長度不足,補0
            data.append(0)
        
        print(data[0],data[-1])
        
        data=np.array([data])
        data=(data-mean)/std
        status_label=model.predict_classes(data)
        print(label_name[status_label[0]])
        
        if label_name[status_label[0]]=='on':
            led.value(1)
        elif label_name[status_label[0]]=='off':
            led.value(0)
            
    time.sleep_us(500)


