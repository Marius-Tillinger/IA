import numpy as np
from sklearn.naive_bayes import GaussianNB
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
train_images = train_images.reshape(train_images.shape[0], 224*224)
val_images = np.array(val_images)
val_images = val_images.reshape(val_images.shape[0], 224*224)
train_labels = np.array(train_labels)
val_labels = np.array(val_labels)

print(train_images[0].shape)
print(train_images[0])

model = GaussianNB()
gb = model.fit(train_images, train_labels)

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

acc = gb.score(val_images, val_labels)
print(acc)