import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from matplotlib import pyplot as plt
import PIL as pillow
from PIL import Image, ImageOps


f = open('train_labels.txt', 'r')
dir = 'data/'
train_data = f.read()
train_data = train_data.split('\n')
train_labels = []
train_images = []
for line in train_data[1:]:
    line = line.split(',')
    if isinstance(line,list) and line[0]:
        x = line[0]
        img = pillow.Image.open(dir + x + '.png')
        img = ImageOps.grayscale(img)
        img = np.array(img)
        img = img / 255.0
        train_images.append(img)
        y = int(line[1])  
        train_labels.append(y)

f.close()

f = open('validation_labels.txt', 'r')
dir = 'data/'
val_data = f.read()
val_data = val_data.split('\n')
val_labels = []
val_images = []
for line in val_data[1:]:
    line = line.split(',')
    if isinstance(line,list) and line[0]:
        x = line[0]
        img = pillow.Image.open(dir + x + '.png')
        img = ImageOps.grayscale(img)
        img = np.array(img)
        img = img / 255.0
        val_images.append(img)
        y = int(line[1])  
        val_labels.append(y)

f.close()

train_images = np.array(train_images)
val_images = np.array(val_images)
train_labels = np.array(train_labels)
val_labels = np.array(val_labels)

model = Sequential()

model.add(Conv2D(64, (3,3), 1, activation='relu', input_shape=(224,224,1)))
model.add(MaxPooling2D(2,2))
model.add(Dropout(0.2))
model.add(Conv2D(16, (3,3), 1, activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Flatten())
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])

cnn = model.fit(train_images, train_labels, epochs=1, batch_size=64)

f = open('sample_submission.txt', 'r')
dir = 'data/'
submission_data = f.read()
submission_data = submission_data.split('\n')
sub = open('submission.csv', 'w')
sub.write('id,class\n')

for line in submission_data[1:]:
    line = line.split(',')
    if isinstance(line,list) and line[0]:
        x = line[0]
        img = pillow.Image.open(dir + x + '.png')
        img = ImageOps.grayscale(img)
        img = np.array(img)
        img = img / 255.0
        res = model.predict(np.array([img]))[0][0]
        if res > 0.1492:
            res = 1
        else:
            res = 0
        sub.write(x + ',' + str(res) + '\n')

sub.close()
f.close()

ev = model.evaluate(val_images, val_labels)
print(ev)

pred = model.predict(val_images)

confusion_matrix = metrics.confusion_matrix(val_labels, pred.round())
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.show()

plt.plot(cnn.history['accuracy'], label='Training Accuracy')
plt.title('Training Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()