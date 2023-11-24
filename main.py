import qrcode
from pyzbar import pyzbar
import cv2
import numpy as np
import os
import barcode
from barcode.writer import ImageWriter

filename = 'qr.png'
bar_filename = 'barcode'
qr_filename = 'qr'
bar_filename_full = 'barcode.png'
path = '/Users/alfa/PycharmProjects/qrlab/'
answers = {0: "неуспешно декодировано", 1: "успешно декодировано"}
example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
example_barcode = "123456789012"


def make_dir(dir_name):
    try:
        os.mkdir(path + dir_name)
    except OSError:
        print("directory " + dir_name + " exists")


def make_bar_code(value):
    try:
        int(value)
    except OSError:
        print("Штрих код состоит только из цифр")

    ean = barcode.get_barcode_class('ean13')
    ean2 = ean(value, writer=ImageWriter())
    print(ean2)
    ean2.save(bar_filename)


def make_qr_code(value):
    qr = qrcode.QRCode(version=3, # это целое число от 1 до 40, которое контролирует размер QR-кода (самый маленький version=1 представляет собой матрицу 21x21)
                       box_size=10, # количество пикселей в каждом "квадрате" QR-кода, разрешение картинки
                       border=2)
    qr.add_data(value)
    qr_img = qr.make_image(back_color='white', fill_color='black')
    qr_img.save(filename)


def decode_code(qr_img):
    codes = pyzbar.decode(qr_img)
    if len(codes) == 0:
        return None
    return codes[0].data.decode('utf-8')


def paint(name, context, code_type, step=1):
    dir_name = code_type + '/' + 'paint'
    make_dir(dir_name)
    img = cv2.imread(name)
    (h, w) = img.shape[:2]
    l = step
    (cX, cY) = (w // 2, h // 2)
    while l > 0:
        paint_img = img
        paint_img[cX - l:cX + l, cY - l:cY + l] = 0
        if decode_code(paint_img) != context:
            cv2.imwrite(os.path.join(path, dir_name + '/none_' + name), paint_img)
            print(l)
            # cv2.imwrite(os.path.join(path, dir_name + '/done_' + name),
            #             img[cX - (l + step):cX + (l + step), cY - (l + step):cY + (l + step)])
            break
        l += step


def zip_code(name, context, code_type, step=1):
    dir_name = code_type + '/' + 'zip'
    make_dir(dir_name)
    img = cv2.imread(name)
    (w, h) = img.shape[:2]
    h -= step
    w -= step
    zip_img = cv2.resize(img, (h, w))
    while True:
        if decode_code(zip_img) == context:
            h -= step
            w -= step
            zip_img = cv2.resize(img, (h, w))
        else:
            break

    cv2.imwrite(os.path.join(path, dir_name + '/none_' + name), zip_img)
    cv2.imwrite(os.path.join(path, dir_name + '/done_' + name),
                cv2.resize(img, (h + step, w + step)))


def brightness_increase(name, context, code_type, step=1, gamma=15):
    dir_name = code_type + '/' + 'brightness'
    make_dir(dir_name)
    img = cv2.imread(name)
    br_img = cv2.addWeighted(img, 1, np.zeros_like(img), 0, gamma)
    while True:
        if decode_code(br_img) == context:
            gamma += step
            br_img = cv2.addWeighted(img, 1, np.zeros_like(img), 0, gamma)
        else:
            break

    cv2.imwrite(os.path.join(path, dir_name + '/none_' + name), br_img)
    cv2.imwrite(os.path.join(path, dir_name + '/done_' + name),
                cv2.addWeighted(img, 1, np.zeros_like(img), 0, gamma-step))


def rotate(name, context, code_type, step=5):
    dir_name = code_type + '/' + 'rotate'
    make_dir(dir_name)
    img = cv2.imread(name)
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    done_angles = []
    none_angles = []
    for angle in range(0, 360, step):
        M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        if decode_code(rotated) != context:
            cv2.imwrite(os.path.join(path, dir_name + "/none_" + str(angle) + "_" + name), rotated)
            none_angles.append(angle)
        else:
            cv2.imwrite(os.path.join(path, dir_name + "/done_" + str(angle) + "_" + name), rotated)
            done_angles.append(angle)
    print("Углы с успешным декодированием:", ', '.join(map(str, done_angles)))
    print("Углы с неудачным декодированием:", ', '.join(map(str, none_angles)))


def flip(name, context, code_type):
    dir_name = code_type + '/' + 'flip'
    make_dir(dir_name)
    img = cv2.imread(name)
    horizontal_flip_img = cv2.flip(img, 1)
    vertical_flip_img = cv2.flip(img, 0)
    cv2.imwrite(os.path.join(path, dir_name + "/horizontal_flip_" + name), horizontal_flip_img)
    cv2.imwrite(os.path.join(path, dir_name + "/vertical_flip" + name), vertical_flip_img)

    print("Отражение по горизонтали - ", answers[decode_code(horizontal_flip_img) == context])
    print("Отражение по вертикали - ", answers[decode_code(vertical_flip_img) == context])


def blur(name, context, code_type, step=1, core_item=1):
    dir_name = code_type + '/' + 'blur'
    make_dir(dir_name)
    img = cv2.imread(name)
    blur_img = cv2.blur(img, (core_item, core_item))
    while True:
        d = decode_code(blur_img)
        if d == context:
            core_item += step
            blur_img = cv2.blur(img, (core_item, core_item))
        else:
            break

    cv2.imwrite(os.path.join(path, dir_name + '/none_' + name), blur_img)
    cv2.imwrite(os.path.join(path, dir_name + '/done_' + name),
                cv2.blur(img, (core_item - step, core_item - step)))


def center_crop(name, context, code_type, step=5):
    dir_name = code_type + '/' + 'center_crop'
    make_dir(dir_name)
    img = cv2.imread(name)
    (h, w) = img.shape[:2]
    l = min(h, w)//2 - step
    (cX, cY) = (w // 2, h // 2)
    while l > 0:
        cropped_img = img[cX - l:cX + l, cY - l:cY + l]
        if decode_code(cropped_img) != context:
            cv2.imwrite(os.path.join(path, dir_name + '/none_' + name), cropped_img)
            cv2.imwrite(os.path.join(path, dir_name + '/done_' + name),
                        img[cX - (l + step):cX + (l + step), cY - (l + step):cY + (l + step)])
            break
        l -= step


def side_crop(name, context, code_type, angle, step=5):
    side_dict = {
        0: "left_up_",
        90: "right_up_",
        180: "right_down_",
        270: "left_down_"
    }
    dir_name = code_type + '/' + 'side_crop'
    make_dir(dir_name)
    img = cv2.imread(name)
    (h, w) = img.shape[:2]
    l = min(h, w) - step
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    rotated_img = cv2.warpAffine(img, M, (w, h))
    while l > 0:
        cropped_img = rotated_img[:l, :l]
        if decode_code(cropped_img) != context:
            M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
            cv2.imwrite(os.path.join(path, dir_name + '/none_' + side_dict[angle] + name),
                        cv2.warpAffine(cropped_img, M, (w, h)))
            cv2.imwrite(os.path.join(path, dir_name + '/done_' + side_dict[angle] + name),
                        cv2.warpAffine(rotated_img[:l + 1, :l + 1], M, (w, h)))
            break
        l -= step


def make_augmentations(filename, context, code_type):
    make_dir(code_type)
    brightness_increase(filename, context, code_type)
    rotate(filename, context, code_type)
    flip(filename, context, code_type)
    blur(filename, context, code_type)
    center_crop(filename, context, code_type)
    side_crop(filename, context, code_type, 0)
    side_crop(filename, context, code_type, 90)
    side_crop(filename, context, code_type, 180)
    side_crop(filename, context, code_type, 270)
    zip_code(filename, context, code_type)
    paint(filename, context, code_type)


if __name__ == '__main__':
    context = input("Введите данные для формирования qr-кода: ")
    if context == "":
        context = example_url
    make_qr_code(context)
    decode_context = decode_code(cv2.imread(filename))
    print("Декодированный код: ", decode_context)
    make_augmentations(filename, context, qr_filename)
    context_to_barcode = input("Введите 12-ти значное число для формирования штрих-кода: ")
    if context_to_barcode == "":
        context_to_barcode = example_barcode
    make_bar_code(context_to_barcode)
    decode_code(cv2.imread(bar_filename_full))
    make_augmentations(bar_filename_full, decode_code(cv2.imread(bar_filename_full)), bar_filename)