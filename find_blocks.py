import os
import argparse
from functools import partial
from concurrent.futures import ProcessPoolExecutor

import cv2
import numpy as np


def find_and_draw_borders(input_image_path, output_image_path):
    # Load image
    image = cv2.imread(input_image_path)
    if image is None:
        raise FileNotFoundError("Specified image does not exist at the path.")

    # To grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List where the final outlines to be drawn will be stored
    final_contours = []

    for contour in contours:
        # Calculate the bounding rectangle for the current path
        x, y, w, h = cv2.boundingRect(contour)
        current_rect = (x, y, x + w, y + h)

        # Checking whether this contour is completely contained within another
        is_contained = False
        for other_contour in contours:
            if np.array_equal(contour, other_contour):
                continue  # We skip comparing the contour with itself
            ox, oy, ow, oh = cv2.boundingRect(other_contour)
            other_rect = (ox, oy, ox + ow, oy + oh)
            if (current_rect[0] >= other_rect[0] and current_rect[2] <= other_rect[2] and
                    current_rect[1] >= other_rect[1] and current_rect[3] <= other_rect[3]):
                is_contained = True
                break

        if not is_contained:
            final_contours.append(contour)

    for contour in final_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite(output_image_path, image)


def process_proxy(image, src, dest):
    src = os.path.join(src, image)
    dest = os.path.join(dest, image)
    find_and_draw_borders(src, dest)


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
    parser = argparse.ArgumentParser(description="Find blocks contours")
    parser.add_argument('--source_dir', type=str, required=True, help="Directory containing images")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the images")
    args = parser.parse_args()
    process_dir_images(args.source_dir, args.output_dir)


if __name__ == "__main__":
    main()
