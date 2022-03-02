import adafruit_trellism4
import adafruit_adxl34x
import board
from busio import I2C
import neopixel
import adafruit_dotstar

trellis = adafruit_trellism4.TrellisM4Express()
accel = adafruit_adxl34x.ADXL343(I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA))
pixel = adafruit_dotstar.DotStar(board.DOTSTAR_CLOCK,board.DOTSTAR_DATA, 1)
accel.enable_tap_detection(tap_count = 2, threshold = 30)
pressed = []
pixeldata = []

drawing = True
clearing = False
X = [(0, 0), (3, 0), (1, 1), (2, 1), (1, 2), (2, 2), (0, 3), (3, 3)]

COLORS = [(255, 255, 255), (255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255,105,180), (148, 0, 211)]
color = [255, 255, 255, 0]
_sel = 0


def update_drawing():
    global pressed, drawing, pixeldata
    pixel.fill([int(x*[1, 0.3, 0.05][color[3]]) for x in color[:3]])
    for k in trellis.pressed_keys:
        if k not in pressed:
            pressed.append(k)
    for k in pressed:
        if k not in trellis.pressed_keys:
            pressed.remove(k)
            if trellis.pixels[k] != tuple([int(x*[1, 0.3, 0.05][color[3]]) for x in color[:3]]):
                trellis.pixels[k] = [int(x*[1, 0.3, 0.05][color[3]]) for x in color[:3]]
            else:
                trellis.pixels[k] = (0, 0, 0)
    if accel.events["tap"]:
        pixeldata = []
        for y in range(4):
            for x in range(8):
                pixeldata.append(trellis.pixels[x, y])
        trellis.pixels.fill((0, 0, 0))
        trellis.pixels.auto_write = False
        drawing = False


def update_menu():
    global color, pressed, _sel, drawing, pixeldata, clearing
    pixel.fill((0, 0, 0))
    for c, col in enumerate(COLORS):
        trellis.pixels[c, 3] = [int(x*0.075) for x in col]
    trellis.pixels[_sel, 3] = color
    for p in range(3):
        trellis.pixels[0, p] = [int(x*[1, 0.3, 0.05][p]) for x in color[:3]]
        trellis.pixels[1, p] = (0, 0, 0)
    trellis.pixels[1, color[3]] = (255, 255, 255)
    trellis.pixels[7, 0] = (255, 0, 0)
    
    for k in trellis.pressed_keys:
        if k not in pressed:
            pressed.append(k)
    for k in pressed:
        if k not in trellis.pressed_keys:
            pressed.remove(k)
            if k[1] == 3:
                color = [COLORS[k[0]][0], COLORS[k[0]][1], COLORS[k[0]][2], color[3]]
                _sel = k[0]
            elif k == (7, 0):
                clearing = True
            elif k[0] == 0 or k[0] == 1:
                color[3] = k[1]
    trellis.pixels.show()

    if accel.events["tap"]:
        trellis.pixels.auto_write = True
        trellis.pixels.fill((0, 0, 0))
        for y in range(4):
            for x in range(8):
                trellis.pixels[x, y] = pixeldata[((8 * y) + x)]
        drawing = True

def update_x():
    global pressed, clearing, drawing
    trellis.pixels.fill((0, 0, 0))
    for p in X:
        trellis.pixels[p] = (255, 255, 255)
    trellis.pixels[6, 1] = (255, 0, 0)
    trellis.pixels[6, 2] = (0, 255, 0)
    trellis.pixels.show()
    for k in trellis.pressed_keys:
        if k not in pressed:
            pressed.append(k)
    for k in pressed:
        if k not in trellis.pressed_keys:
            pressed.remove(k)
            if k == (6, 1):
                trellis.pixels.fill((0, 0, 0))
                clearing = False
            elif k == (6, 2):
                clearing = False
                drawing = True
                trellis.pixels.auto_write = True
                trellis.pixels.fill((0, 0, 0))
        

while True:
    if drawing:
        update_drawing()
    else:
        if clearing:
            update_x()
        else:
            update_menu()
