import qrcode
from pyzbar import pyzbar
import cv2
import numpy as np
import os

filename = 'qr.png'
path = '/Users/alfa/PycharmProjects/qrlab/'
answers = {0: "неуспешно декодировано", 1: "успешно декодировано"}
# example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def make_dir(dir_name):
    try:
        os.mkdir(path + dir_name)
    except OSError:
        print("directory " + dir_name + " exists")


def make_qr_code(value):
    qr = qrcode.QRCode(version=3, box_size=10, border=2)
    qr.add_data(value)
    qr_img = qr.make_image(back_color='white', fill_color='black')
    qr_img.save(filename)


def decode_qr(qr_img):
    codes = pyzbar.decode(qr_img)
    if len(codes) == 0:
        return None
    return codes[0].data.decode('utf-8')


def brightness_increase(name, context, step=1, gamma=15):
    dir_name = 'brightness'
    make_dir(dir_name)
    img = cv2.imread(name)
    br_img = cv2.addWeighted(img, 1, np.zeros_like(img), 0, gamma)
    while True:
        if decode_qr(br_img) == context:
            gamma += step
            br_img = cv2.addWeighted(img, 1, np.zeros_like(img), 0, gamma)
        else:
            break

    cv2.imwrite(os.path.join(path, dir_name + '/none_' + filename), br_img)
    cv2.imwrite(os.path.join(path, dir_name + '/done_' + filename),
                cv2.addWeighted(img, 1, np.zeros_like(img), 0, gamma-step))


def rotate(name, context, step=5):
    dir_name = 'rotate'
    make_dir(dir_name)
    img = cv2.imread(name)
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    done_angles = []
    none_angles = []
    for angle in range(0, 360, step):
        M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        if decode_qr(rotated) != context:
            cv2.imwrite(os.path.join(path, dir_name + "/none_" + str(angle) + "_" + filename), rotated)
            none_angles.append(angle)
        else:
            cv2.imwrite(os.path.join(path, dir_name + "/done_" + str(angle) + "_" + filename), rotated)
            done_angles.append(angle)
    print("Углы с успешным декодированием:", ', '.join(map(str, done_angles)))
    print("Углы с неудачным декодированием:", ', '.join(map(str, none_angles)))


def flip(name, context):
    dir_name = 'flip'
    make_dir(dir_name)
    img = cv2.imread(name)
    horizontal_flip_img = cv2.flip(img, 1)
    vertical_flip_img = cv2.flip(img, 0)
    cv2.imwrite(os.path.join(path, dir_name + "/horizontal_flip_" + filename), horizontal_flip_img)
    cv2.imwrite(os.path.join(path, dir_name + "/vertical_flip" + filename), vertical_flip_img)

    print("Отражение по горизонтали - ", answers[decode_qr(horizontal_flip_img) == context])
    print("Отражение по вертикали - ", answers[decode_qr(vertical_flip_img) == context])


def blur(name, context, step=1, core_item=1):
    dir_name = 'blur'
    make_dir(dir_name)
    img = cv2.imread(name)
    blur_img = cv2.blur(img, (core_item, core_item))
    while True:
        if decode_qr(blur_img) == context:
            core_item += step
            blur_img = cv2.blur(img, (core_item, core_item))
        else:
            break

    cv2.imwrite(os.path.join(path, dir_name + '/none_' + filename), blur_img)
    cv2.imwrite(os.path.join(path, dir_name + '/done_' + filename),
                cv2.blur(img, (core_item - step, core_item - step)))


def center_crop(name, context, step=5):
    dir_name = 'center_crop'
    make_dir(dir_name)
    img = cv2.imread(name)
    (h, w) = img.shape[:2]
    l = min(h, w)//2 - step
    (cX, cY) = (w // 2, h // 2)
    while l > 0:
        cropped_img = img[cX - l:cX + l, cY - l:cY + l]
        l -= step
        if decode_qr(cropped_img) != context:
            cv2.imwrite(os.path.join(path, dir_name + '/none_' + filename), cropped_img)
            cv2.imwrite(os.path.join(path, dir_name + '/done_' + filename),
                        img[cX - l + 1:cX + l + 1, cY - l + 1:cY + l + 1])
            break


def side_crop(name, context, angle, step=5):
    side_dict = {
        0: "left_up_",
        90: "right_up_",
        180: "right_down_",
        270: "left_down_"
    }
    dir_name = 'side_crop'
    make_dir(dir_name)
    img = cv2.imread(name)
    (h, w) = img.shape[:2]
    l = min(h, w) - step
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    rotated_img = cv2.warpAffine(img, M, (w, h))
    while l > 0:
        cropped_img = rotated_img[:l, :l]
        if decode_qr(cropped_img) != context:
            M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
            cv2.imwrite(os.path.join(path, dir_name + '/none_' + side_dict[angle] + filename),
                        cv2.warpAffine(cropped_img, M, (w, h)))
            cv2.imwrite(os.path.join(path, dir_name + '/done_' + side_dict[angle] + filename),
                        cv2.warpAffine(rotated_img[:l + 1, :l + 1], M, (w, h)))
            break
        l -= step


def make_augmentations(filename, context):
    brightness_increase(filename, context)
    rotate(filename, context)
    flip(filename, context)
    blur(filename, context)
    center_crop(filename, context)
    side_crop(filename, context, 0)
    side_crop(filename, context, 90)
    side_crop(filename, context, 180)
    side_crop(filename, context, 270)


if __name__ == '__main__':
    context = input("Введите данные для формирования qr-кода: ")
    make_qr_code(context)
    decode_context = decode_qr(cv2.imread(filename))
    print("Декодированный код: ", decode_context)
    make_augmentations(filename, context)