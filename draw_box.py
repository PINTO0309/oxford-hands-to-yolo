#!/usr/bin/env python

import cv2
import os
import sys
import random
import argparse
from natsort import natsorted

label_folder = 'hand_dataset/training_dataset/training_data/new_annotations/'
raw_images_folder = 'hand_dataset/training_dataset/training_data/images/'
save_images_folder = 'save_image/'
name_list_path = 'name_list.txt'
classes_path = 'classes.txt'


def plot_one_box(x, image, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(image, c1, c2, color, thickness=1, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)
        cv2.putText(image, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def draw_box_on_image(
    image_path,
    txt_path,
    classes,
    colors,
):
    # flag_people_or_car_data = 0
    source_file = open(txt_path)
    image = cv2.imread(image_path)
    try:
        height, width, channels = image.shape
    except:
        print('no shape info.')
        return 0

    box_number = 0
    for line in source_file:
        staff = line.split()
        class_idx = int(staff[0])

        x_center, y_center, w, h = float(staff[1])*width, float(staff[2])*height, float(staff[3])*width, float(staff[4])*height
        x1 = round(x_center-w/2)
        y1 = round(y_center-h/2)
        x2 = round(x_center+w/2)
        y2 = round(y_center+h/2)

        plot_one_box([x1,y1,x2,y2], image, color=colors[class_idx], label=classes[class_idx], line_thickness=None)
        box_number += 1

    return box_number, image



def make_name_list(raw_images_folder, name_list_path):
    image_file_list = natsorted(os.listdir(raw_images_folder))
    with open(name_list_path, 'w') as text_image_name_list_file:
        for  image_file_name in image_file_list:
            image_name, file_extend = os.path.splitext(image_file_name)
            text_image_name_list_file.write(image_name+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v',
        '--enable_image_view',
        action='store_true',
    )
    parser.add_argument(
        '-s',
        '--enable_image_save',
        action='store_true',
    )
    args = parser.parse_args()
    enable_image_view = args.enable_image_view
    enable_image_save = args.enable_image_save
    if not enable_image_view and not enable_image_save:
        print('Either enable_image_view or enable_image_save must be specified.')
        sys.exit(0)

    make_name_list(raw_images_folder, name_list_path)
    classes = image_names = open(classes_path).read().strip().split()
    random.seed(42)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))]
    image_names = open(name_list_path).read().strip().split()
    box_total = 0
    image_total = 0

    while True:
        image_name = image_names[image_total]
        if 'DS_Store' in image_name:
            image_total += 1
            continue
        txt_path  = os.path.join(label_folder, f'{image_name}.txt'%())
        image_path = os.path.join( raw_images_folder, f'{image_name}.jpg')
        save_file_path = os.path.join(save_images_folder, f'{image_name}.jpg')
        box_num, image = draw_box_on_image(
            image_path,
            txt_path,
            classes,
            colors,
        )

        if enable_image_view:
            cv2.imshow('Viewer', image)

        key = cv2.waitKey(0)
        if key == 27:  # ESC
            break

        elif key == 100: # d
            os.remove(save_file_path)
            image_total += 1

        elif key == 106: # j
            image_total -= 1

        else:
            if enable_image_save:
                os.makedirs(os.path.dirname(save_file_path), exist_ok=True)
                cv2.imwrite(save_file_path, image)
            box_total += box_num
            image_total += 1

