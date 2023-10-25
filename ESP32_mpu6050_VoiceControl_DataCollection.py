from machine import Pin,ADC,PWM
import time

led=Pin(32,Pin.OUT,value=0)
horn=PWM(Pin(14),duty=0,freq=2000)
button_yes=Pin(12,Pin.IN,Pin.PULL_UP)
button_no=Pin(13,Pin.IN,Pin.PULL_UP)

adc=ADC(Pin(36))
adc.width(ADC.WIDTH_12BIT)     # 解析度12BT
adc.atten(ADC.ATTN_11DB)       # 最大電壓36V

f=open('on.txt','w')

for i in range(100):           # 100筆資料
    time.sleep(0.1)
    if(i>=100/2):
        led.value(1)           # 紀錄次數過半,開燈
        
    print('\n第'+str(i+1)+'筆')
    while True:
        sound=adc.read()       # 接收聲音資訊
        if(sound>100):         # ADC>100才紀錄,避免環境音誤觸
            print('\n action')
            no_sound=0
            data=[sound]
            # 沒聲音次數少於150次或超過資料儲存量400+150
            while(no_sound<150 and len(data)<550):
                sound=adc.read()
                data.append(sound)
                if(sound==0):
                    no_sound+=1
                else:
                    no_sound=0
                time.sleep_us(500)
            data=data[:-150]
            
            if(len(data)<150):
                print('Noise,try again')
                continue
            # 播放音效
            for j in data:
                horn.duty(int(j/4))
                time.sleep_us(500)
            
            print(len(data))
            while(len(data)<400):  # 資料長度不足,補0
                data.append(0)
            
            horn.duty(0)           # 關閉聲音
            
            print('Save or Delete?',end=' ')
            while(button_yes.value()==1 and
                  button_no.value()==1):
                time.sleep(0.01)
            
            if(button_yes.value()==0):
                f.write(str(data)[1:-1]+'\n')
                print('Save')
                break
            elif(button_no.value()==0):
                print('Delete')
                time.sleep(0.1)    # 避免出現雜訊
                print('Try again')
        
        time.sleep_us(500)
led.value(0)                       # 關燈
f.close()
            




