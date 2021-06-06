import board
import neopixel
import time

MAX_LED_LENGTH = 9

def stripe(red=0,green=0,blue=0):
    for x in range(0, MAX_LED_LENGTH):
        pixels[x] = (red, green, blue)
        time.sleep(1)

def cleanup():
    pixels.fill((0, 0, 0))

def main():
    try:
        stripe(0, 255, 0)

    finally:
        cleanup()

if __name__ == "__main__":
    pixels = neopixel.NeoPixel(board.D18, 30)
    main()