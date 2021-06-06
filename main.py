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

MAX_LED_LENGTH = 14

def stripe(red=0,green=0,blue=0):
    for x in range(0, MAX_LED_LENGTH):
        pixels[x] = (red, green, blue)
        time.sleep(0.1)

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
    stripe(rgb[0], rgb[1], rgb[2])

def main():
    try:
        client = mqtt.Client()
        client.username_pw_set("token:%s"%TOKEN)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(HOSTNAME, port=PORT, keepalive=60)
        client.loop_forever()
        # stripe(0, 255, 0)
        # while True:
        #     lightUp(0, 255, 0)

    finally:
        cleanup()

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.D18, 30)
    main()