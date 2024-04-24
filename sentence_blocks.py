import os
import argparse
from functools import partial
from concurrent.futures import ProcessPoolExecutor

import pytesseract
import cv2
import numpy as np


def draw_text_rectangles(image_path, output_path):
    # Загрузить изображение с помощью OpenCV
    image = cv2.imread(image_path)
    # Переводим изображение в формат, совместимый для обработки Tesseract
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Использовать pytesseract для получения информации о расположении каждого предложения
    data = pytesseract.image_to_data(rgb_image, output_type=pytesseract.Output.DICT)

    current_sentence = ""
    sentence_start = None

    # Пройти по данным и рисовать прямоугольники вокруг предложений
    for i in range(len(data['text'])):
        if data['text'][i].strip():
            if current_sentence == "":
                sentence_start = i
            current_sentence += data['text'][i] + ' '
            # Если встретился конец предложения, рисуем прямоугольник
            if current_sentence.strip()[-1] in '.!?':
                x, y, w, h = data['left'][sentence_start], data['top'][sentence_start], data['width'][sentence_start], \
                data['height'][sentence_start]
                for j in range(sentence_start + 1, i + 1):
                    x = min(x, data['left'][j])
                    y = min(y, data['top'][j])
                    w = max(x + w, data['left'][j] + data['width'][j]) - x
                    h = max(y + h, data['top'][j] + data['height'][j]) - y
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Рисуем красный прямоугольник
                current_sentence = ""
                sentence_start = None

    # Сохранить измененное изображение
    cv2.imwrite(output_path, image)


def process_proxy(image, src, dest):
    src = os.path.join(src, image)
    dest = os.path.join(dest, image)
    draw_text_rectangles(src, dest)


def process_dir_images(source_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    process = partial(process_proxy, src=source_dir, dest=output_dir)

    images = os.listdir(source_dir)
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
        res = pool.map(process, images)
        list(res)


def main():
    parser = argparse.ArgumentParser(description="Find sentences")
    parser.add_argument('--source_dir', type=str, required=True, help="Directory containing images")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the images")
    args = parser.parse_args()
    process_dir_images(args.source_dir, args.output_dir)


if __name__ == "__main__":
    main()
