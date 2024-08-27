from enum import Enum

from PIL import ImageOps, Image
from tqdm import tqdm
import numpy as np

import glob


class Dataset(Enum):
    TRAIN = "../datasets/chest_Xray/train/"
    TEST = "../datasets/chest_Xray/test/"
    VAL = "../datasets/chest_Xray/val/"


class Values(Enum):
    NORMAL = 0
    PNEUMONIA = 1


def import_dataset(dataset_type, img_length):
    print("Loading dataset " + dataset_type.value)
    images = []
    for rayX_type in Values:
        new_images = glob.glob(dataset_type.value + rayX_type.name + '/*.jpeg')
        images += new_images
    dataset_x = [[[None]*img_length]*img_length]*len(images)
    dataset_y = [None]*len(images)
    for i in tqdm(range(len(images)), desc="Importing images", colour="green"):
        img = Image.open(images[i])
        if img.mode != "L":
            img = ImageOps.grayscale(img)
        resized_img = ImageOps.pad(img, (img_length, img_length))
        arr_img = np.asarray(resized_img)
        dataset_x[i] = arr_img
        if "pneumonia" in images[i].lower():
            dataset_y[i] = 1
        elif "normal" in images[i].lower():
            dataset_y[i] = 0

    print("Returning processed data")
    dataset_x = np.array(dataset_x)
    dataset_y = np.array(dataset_y)
    return dataset_x, dataset_y


def format_dataset(data_x, img_length):
    print("Reshaping data to 1D array")
    data_x = data_x.reshape(len(data_x), img_length * img_length)
    print("Changing type to float")
    data_x = data_x.astype('float32')
    print("Normalize data")
    data_x /= 255
    return data_x
