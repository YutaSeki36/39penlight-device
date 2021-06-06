import board
import neopixel
import time

MAX_LED_LENGTH = 14

def stripe(red=0,green=0,blue=0):
    for x in range(0, MAX_LED_LENGTH):
        pixels[x] = (red, green, blue)
        time.sleep(0.1)

def lightUp(red=0,green=0,blue=0):
    pixels.fill((red, green, blue))

def cleanup():
    pixels.fill((0, 0, 0))

def main():
    try:
        stripe(0, 255, 0)
        while True:
            lightUp(0, 255, 0)

    finally:
        cleanup()

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.D18, 30)
    main()