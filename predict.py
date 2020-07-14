import glob
from PIL import Image
import numpy as np
import tensorflow as tf
import datetime

model = tf.keras.models.load_model('model1.h5')

threshold = 60

num = []

for path in sorted(glob.glob('imgs/*')):
    img = Image.open(path)
    img.save('./trash/raw-' + path[5:])

    img = img.convert('L').resize((28, 28))
    img = np.array(img)
    img = (img > threshold) * 255
    img = 255 - img.astype('uint8')

    Image.fromarray(img).save('./trash/baked-' + path[5:])

    img = img.astype('float32') / 255
    img = img.reshape((1,) + img.shape + (1,))
    pred = model.predict(img)
    num.append(np.argmax(np.array(pred)))

for i, j in enumerate(num):
    print(str(j), end='')
    if i != len(num) - 1:
        print(" + ", end='')
print(" = " + str(sum(num)))
