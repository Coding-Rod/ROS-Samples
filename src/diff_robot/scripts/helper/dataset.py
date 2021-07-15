import os
import shutil
import random

path = "/home/rigu/imp342p2_ws/src/diff_robot/scripts/raw_data/"
# Hydrant
training_hydrant = "/home/rigu/imp342p2_ws/src/data/train/fire/"
validation_hydrant = "/home/rigu/imp342p2_ws/src/data/validation/fire/"
# Bookshelf
training_bookshelf = "/home/rigu/imp342p2_ws/src/data/train/book/"
validation_bookshelf = "/home/rigu/imp342p2_ws/src/data/validation/book/"
# None
training_none = "/home/rigu/imp342p2_ws/src/data/train/nada/"
validation_none = "/home/rigu/imp342p2_ws/src/data/validation/nada/"

dir_list = os.listdir(path)

for files in dir_list:
    print(files.split('-')[0])
    ind = random.randint(0, 99)
    if files.split('-')[0] == 'fire':
        if ind <= 80:  # training 80% - validation 20%
            shutil.copy(path + '/' + files, training_hydrant)
        else:
            shutil.copy(path + '/' + files, validation_hydrant)
    elif files.split('-')[0] == 'book':
        if ind <= 80:
            shutil.copy(path + '/' + files, training_bookshelf)
        else:
            shutil.copy(path + '/' + files, validation_bookshelf)
    elif files.split('-')[0] == 'nada':
        if ind <= 80:
            shutil.copy(path + '/' + files, training_none)
        else:
            shutil.copy(path + '/' + files, validation_none)
