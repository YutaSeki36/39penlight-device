import board
import neopixel
import time
import os
import subprocess
import paho.mqtt.client as mqtt
import config

HOSTNAME = "mqtt.beebotte.com"
PORT = 1883
TOKEN = config.TOKEN
TOPIC = "penlight/color"

MAX_LED_LENGTH = 15

class FlushTypeEnum(Enum):
    NORMAL = 1
    WAVE = 2

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
            self.lightUpComp = True
            if self.flush_type == FlushTypeEnum.NORMAL: 
                    for x in range(0, MAX_LED_LENGTH):
                        pixels[x] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                        time.sleep(0.1)
            else:
                pos = 0
                while not(self.kill_flag):
                    if self.lightUpComp:
                        break
                    pixels[pos] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                    if pos == MAX_LED_LENGTH:
                        pixels[0] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                    else:
                        pixels[pos+1] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                    time.sleep(0.05)
                    pos+=1

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

def on_connect(client, userdata, flags, respons_code):
    print('status {}'.format(respons_code))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(msg.payload.decode('utf-8'))
    rgb = hex_to_rgb(msg.payload.decode('utf-8'))
    t.flush_color_red = rgb[0]
    t.flush_color_green = rgb[1]
    t.flush_color_blue = rgb[2]
    if t.flush_type == FlushTypeEnum.NORMAL:
        t.flush_type = FlushTypeEnum.WAVE
    else:
        t.lightUpComp = True
        t.flush_type = FlushTypeEnum.NORMAL

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
    main()