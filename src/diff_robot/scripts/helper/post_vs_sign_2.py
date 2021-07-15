import tensorflow as tf
import os
#import shutil
import numpy as np
BATCH_SIZE=32 
#config = tf.compat.v1.ConfigProto()
#config.gpu_options.allow_growth = True
#session = tf.compat.v1.InteractiveSession(config=config) 
#print(os.listdir("data")) 
'''try:
  shutil.rmtree('dat/.ipynb_checkpoints') 
  shutil.rmtree('dat/training/.ipynb_checkpoints') 
  shutil.rmtree('dat/validation/.ipynb_checkpoints')
except:
  print("already deleted")
try:
  shutil.rmtree('dat/training/.ipynb_checkpoints') 
except:
  print("already deleted")
try:
  shutil.rmtree('dat/validation/.ipynb_checkpoints')
except:
  print("already deleted")
print(os.listdir("data")) 
print(os.listdir("dat/training"))
print(os.listdir("dat/validation"))
'''
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0/255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0/255
)

train_generator = train_datagen.flow_from_directory(
    'data/training',
    target_size=(150, 150),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

validation_generator = test_datagen.flow_from_directory(
    'data/validation',
    target_size=(150, 150),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)
train_dir = 'data/training'
validation_dir = 'data/validation'
train_post_dir = os.path.join(train_dir, 'post') 
train_sign_dir = os.path.join(train_dir, 'sign') 
validation_post_dir = os.path.join(validation_dir, 'post') 
validation_sign_dir = os.path.join(validation_dir, 'sign') 

num_post_tr = len(os.listdir(train_post_dir))
num_sign_tr = len(os.listdir(train_sign_dir))

num_post_val = len(os.listdir(validation_post_dir))
num_sign_val = len(os.listdir(validation_sign_dir))

total_train = num_post_tr + num_sign_tr
total_val = num_post_val + num_sign_val

steps_epoch=int(np.ceil(total_train /float(BATCH_SIZE)))
val_steps=int(np.ceil(total_val / float(BATCH_SIZE)))

# Note the input shape is the desired size of the image 300x300 with 3 bytes color # This is the first convolution
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(8, (5, 5), activation='relu', input_shape=(
        150, 150, 3)), tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(
        4, (3, 3), activation='relu'), tf.keras.layers.MaxPooling2D(2, 2),
    # The third convolution
    #tf.keras.layers.Conv2D(
    #    4, (3, 3), activation='relu'), tf.keras.layers.MaxPooling2D(2, 2),
    # The fourth convolution
    #tf.keras.layers.Conv2D(
    #    16, (3, 3), activation='relu'), tf.keras.layers.MaxPooling2D(2, 2),
    # The fifth convolution
    #tf.keras.layers.Conv2D(
    #    8, (3, 3), activation='relu'), tf.keras.layers.MaxPooling2D(2, 2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(4, activation='relu'),
    # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class
    tf.keras.layers.Dense(1, activation='sigmoid')])
model.summary()

model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.RMSprop(lr=0.0001), metrics=['accuracy'])
model.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=3, validation_data=validation_generator, validation_steps=val_steps)
tf.keras.models.save_model(model,"post_vs_sign_2.h5")
