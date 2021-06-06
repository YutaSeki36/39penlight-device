import board
import neopixel
import time
import os
import subprocess
import paho.mqtt.client as mqtt

HOSTNAME = "mqtt.beebotte.com"
PORT = 1883
TOKEN = os.environ.get('TOKEN')
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

def on_connect(client, userdata, flags, respons_code):
    print('status {}'.format(respons_code))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(msg.payload)
    data = json.loads(msg.payload.decode("utf-8"))["data"]
    try:
        execIrrp(data)
    except ValueError as e:
        print(e)

def main():
    client = mqtt.Client()
    client.username_pw_set("token:%s"%TOKEN)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOSTNAME, port=PORT, keepalive=60)
    client.loop_forever()

    try:
        stripe(0, 255, 0)
        while True:
            lightUp(0, 255, 0)

    finally:
        cleanup()

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.D18, 30)
    main()