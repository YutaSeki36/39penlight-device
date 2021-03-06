import board
import neopixel
import time
import os
import subprocess
import paho.mqtt.client as mqtt
import threading
import config
from enum import IntEnum

HOSTNAME = "mqtt.beebotte.com"
PORT = 1883
TOKEN = config.TOKEN
TOPIC = "penlight/color"

MAX_LED_LENGTH = 15

class FlushTypeEnum(IntEnum):
    NORMAL = 1
    WAVE = 2
    BOUND = 3

class ThreadJob(threading.Thread):
    def __init__(self, flush_color_red=0, flush_color_green=0, flush_color_blue=0):
        threading.Thread.__init__(self)
        self.flush_color_red = flush_color_red
        self.flush_color_green = flush_color_green
        self.flush_color_blue = flush_color_blue
        self.kill_flag = False
        self.lightup_comp = False
        self.flush_type = FlushTypeEnum.NORMAL

    def run(self):
        print(self.kill_flag)
        while not(self.kill_flag):
            self.lightUpComp = False
            pixels.fill((0, 0, 0))
            if self.flush_type == FlushTypeEnum.NORMAL: 
                    for x in range(0, MAX_LED_LENGTH):
                        pixels[x] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                        time.sleep(0.05)
                    while not(self.kill_flag):
                        if self.lightUpComp:
                            break
            elif self.flush_type == FlushTypeEnum.WAVE:
                pos = 0
                while not(self.kill_flag):
                    if self.lightUpComp:
                        break
                    pixels.fill((0, 0, 0))
                    pixels[pos] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                    if pos == MAX_LED_LENGTH:
                        pixels[0] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                        pos = 0
                    else:
                        pixels[pos+1] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                    time.sleep(0.05)
                    pos+=1
            elif self.flush_type == FlushTypeEnum.BOUND:
                pos = 0
                up = True
                while not(self.kill_flag):
                    if self.lightUpComp:
                        break
                    pixels.fill((0, 0, 0))
                    pixels[pos] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                    if pos == MAX_LED_LENGTH:
                        up = False
                    if pos == 0 and up == False:
                        up = True
                    if up:
                        pos+=1
                    else:
                        pos-=1
                    time.sleep(0.05)

        print(self.kill_flag)
        time.sleep(0.5)
        cleanup()

def lightUp(red=0,green=0,blue=0):
    pixels.fill((red, green, blue))

def cleanup():
    pixels.fill((0, 0, 0))

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))

def bpm_to_interval(bpm):
    ceil_digit = 2
    interval = bpm / 60
    return math.floor(interval * 10 ** ceil_digit) / (10 ** ceil_digit)

def on_connect(client, userdata, flags, respons_code):
    print('status {}'.format(respons_code))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(msg.payload.decode('utf-8'))
    payload = msg.payload.decode('utf-8').split(',')
    rgb = hex_to_rgb(payload[0])
    t.flush_color_red = rgb[0]
    t.flush_color_green = rgb[1]
    t.flush_color_blue = rgb[2]
    ft = int(payload[1])
    t.lightUpComp = True
    if ft == FlushTypeEnum.NORMAL:
        t.flush_type = FlushTypeEnum.NORMAL
    elif ft == FlushTypeEnum.WAVE:
        t.flush_type = FlushTypeEnum.WAVE
    elif ft == FlushTypeEnum.BOUND:
        t.flush_type = FlushTypeEnum.BOUND

def main():
    try:
        client = mqtt.Client()
        client.username_pw_set("token:%s"%TOKEN)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(HOSTNAME, port=PORT, keepalive=60)
        client.loop_forever()

    finally:
        cleanup()

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.D18, 30)
    t = ThreadJob()
    t.start()
    main()