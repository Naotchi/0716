import time
import picamera
import numpy
from PIL import Image
import RPi.GPIO  # GPIOを扱うためのライブラリを読み込み
from subprocess import run

RPi.GPIO.setmode(RPi.GPIO.BCM)

RPi.GPIO.setup(18, RPi.GPIO.IN)
RPi.GPIO.setup(15, RPi.GPIO.OUT)

def save_image(ndarray):


    """picameraによって画像を格納されたnumpyの配列を受け取り、PILライブラリを使ってファイルとして保存する

    Args:
        ndarray (numpy.ndarray): 画像を格納したnumpy.ndarray型の3次元配列。例えば横3px, 縦2pxで真っ赤の画像は以下のような形式とする
        [[[255, 0, 0], [255, 0, 0], [255, 0, 0]], [[255, 0, 0], [255, 0, 0], [255, 0, 0]]]

    Returns:
        None

    """
    im = Image.fromarray(ndarray)
    im.save('picture.png')
    im.show()


def take_a_picture():
    global cnt
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)  # 撮影する画像の縦横ピクセル
        camera.framerate = 24  # フレームレート
        time.sleep(2)  # カメラのセットアップが終わるのを待つ
        image = numpy.zeros((240, 320, 3), dtype=numpy.uint8)  # numpy.ndarrayという特殊な型(リストに近い)で3次元配列を定義
        camera.capture(image, 'rgb')
        save_image(image)
        print("saved")


RPi.GPIO.output(15, RPi.GPIO.LOW)
print("ready")

while True:
    i = RPi.GPIO.input(18)
    if i == RPi.GPIO.HIGH:
        RPi.GPIO.output(15, RPi.GPIO.HIGH)
        time.sleep(0.5)
        i = RPi.GPIO.input(18)
        if i == RPi.GPIO.HIGH:
            RPi.GPIO.output(15, RPi.GPIO.LOW)
            print("finished")
            break
        take_a_picture()
        RPi.GPIO.output(15, RPi.GPIO.LOW)
    else:
        time.sleep(0.1)

RPi.GPIO.cleanup()