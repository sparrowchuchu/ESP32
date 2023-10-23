from pynput.keyboard import Controller
from pynput.keyboard import Key
import time

my_keyboard=Controller()

my_keyboard.press(Key.up)
my_keyboard.release(Key.up)
time.sleep(1)

my_keyboard.press(Key.down)
my_keyboard.release(Key.down)
time.sleep(1)

my_keyboard.press(Key.left)
my_keyboard.release(Key.left)
time.sleep(1)

my_keyboard.press(Key.right)
my_keyboard.release(Key.right)
time.sleep(1)

