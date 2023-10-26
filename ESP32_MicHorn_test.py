from machine import Pin,ADC,PWM
import time

# 工作週期duty: 設定為0(範圍0~1023)。PWM預設duty為512
# 頻率freq: 設定為6000。PWM預設freq為5000
horn=PWM(Pin(14),duty=0,freq=5000)

button_yes=Pin(12,Pin.IN,Pin.PULL_UP)

adc=ADC(Pin(36))
adc.width(ADC.WIDTH_12BIT)     # 解析度12BT
adc.atten(ADC.ATTN_11DB)       # 最大電壓36V

f=open('on_test.txt','w')

flag=0

while True:
    sound=adc.read()       # 接收聲音資訊
    if(sound>2500):         # ADC>100才紀錄,避免環境音誤觸
        print('\n action')
        no_sound=0
        data=[sound]
        
        # 蒐集聲音(開/關) 
        while no_sound<150 and len(data)<400:
            if(sound==0):
                no_sound+=1
            else:
                no_sound=0
            data.append(adc.read())
            time.sleep_us(500)
                   
        print(len(data))
#         print('press to Play')
#         while button_yes.value()==1:
#             pass
        # 播放音效
        for j in data:
            horn.duty(int(j/4))
            time.sleep_us(500)      
        horn.duty(0)           # 關閉喇叭聲音
        
        f.write(str(data)+'\n')
        
        print('press to continue')
        while button_yes.value()==1:
            pass
        
        if flag>5:
            break
        
        flag+=1
        time.sleep(0.5) 

f.close()


