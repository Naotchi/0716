import glob
from PIL import Image
import numpy as np
import tensorflow as tf
import datetime
import os
import shutil

path = str(datetime.datetime.now())
os.mkdir(path)

model = tf.keras.models.load_model('models/model30.h5')

img = Image.open('picture.png')
shutil.move('picture.png', path + '/raw_picture.png')

img = np.array(img.convert('L'))

threshold = -1
print('please enter threshold')
while True:
    img_can = img.copy()
    threshold_can = int(input())
    if threshold_can == -1:
        break
    img_can = (img_can > threshold_can) * 255
    img_can = 255 - img_can.astype('uint8')
    Image.fromarray(img_can).show()
    threshold = threshold_can

img = (img > threshold) * 255
img = 255 - img.astype('uint8')
Image.fromarray(img).save(path + '/baked-picture.png')

number = 0
for i in range(8):
    l = i * 37
    r = l + 37
    now = img[:37, l:r]
    now_resized = Image.fromarray(now).resize((28, 28))
    now_resized.save(path + '/number-' + str(i) + '.png')
    now_array = np.array(now_resized)
    now_array = now_array.astype('float32') / 255
    now_array = now_array.reshape((1,) + now_array.shape + (1,))
    number += np.argmax(model.predict(now_array)) * 10**(7 - i)

score = 0
for i in range(3):
    l = (i + 5) * 37
    r = l + 37
    now = img[37:74, l:r]
    now_resized = Image.fromarray(now).resize((28, 28))
    now_resized.save(path + '/score-' + str(i) + '.png')
    now_array = np.array(now_resized)
    now_array = now_array.astype('float32') / 255
    now_array = now_array.reshape((1,) + now_array.shape + (1,))
    score += np.argmax(model.predict(now_array)) * 10**(2 - i)

print("学籍番号 : " + str(number))
print("得点 : " + str(score))