import board
import neopixel
import time
import os
import subprocess
import paho.mqtt.client as mqtt
import threading
import config

HOSTNAME = "mqtt.beebotte.com"
PORT = 1883
TOKEN = config.TOKEN
TOPIC = "penlight/color"

MAX_LED_LENGTH = 15


# def stripe(red=0,green=0,blue=0):
#     for x in range(0, MAX_LED_LENGTH):
#         pixels[x] = (red, green, blue)
#         time.sleep(0.2)

class ThreadJob(threading.Thread):
    def __init__(self, flush_color_red=0, flush_color_green=0, flush_color_blue=0):
        threading.Thread.__init__(self)
        self.flush_color_red = flush_color_red
        self.flush_color_green = flush_color_green
        self.flush_color_blue = flush_color_blue
        self.kill_flag = False
        self.lightUpComp = False

    def run(self):
        print(self.kill_flag)
        while not(self.kill_flag):
            if not(self.lightUpComp):
                for x in range(0, MAX_LED_LENGTH):
                    pixels[x] = (self.flush_color_red, self.flush_color_green, self.flush_color_blue)
                    time.sleep(0.2)
        print(self.kill_flag)
        time.sleep(1)
        cleanup()

# def asyncStripe():
#     global flush_color_red
#     global flush_color_green
#     global flush_color_blue
#     for x in range(0, MAX_LED_LENGTH):
#         pixels[x] = (flush_color_red, flush_color_green, flush_color_blue)
#         time.sleep(0.2)

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
    # stripe(rgb[0], rgb[1], rgb[2])

def main():
    # th = threading.Thread(target=asyncStripe)
    # th.start()

    try:
        client = mqtt.Client()
        client.username_pw_set("token:%s"%TOKEN)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(HOSTNAME, port=PORT, keepalive=60)
        client.loop_forever()

    finally:
        t.kill_flag = True

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.D18, 30)
    t = ThreadJob()
    t.start()
    main()