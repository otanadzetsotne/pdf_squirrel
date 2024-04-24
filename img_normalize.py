import os
import argparse
from functools import partial
from concurrent.futures import ProcessPoolExecutor

import cv2
import numpy as np
from skimage.filters import threshold_otsu


def process_document_image(image_path, output_path):
    """
    Processes a document image, removing graphic elements and highlighting text.

    Options:
        image_path (str): Path to the source image file.
        output_path (str): Path to the file to save the processed image.

    Returns:
        bool: True if processing and saving were successful, otherwise False.
    """

    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: can't open image {image_path}")
            return False
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        thresh_val = threshold_otsu(gray)
        binary = gray > thresh_val

        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(binary.astype(np.uint8), cv2.MORPH_OPEN, kernel, iterations=1)

        cv2.imwrite(output_path, (cleaned * 255).astype(np.uint8))
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def process_proxy(image, src, dest):
    src = os.path.join(src, image)
    dest = os.path.join(dest, image)
    process_document_image(src, dest)


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
    parser = argparse.ArgumentParser(description="Convert PDF files to images")
    parser.add_argument('--source_dir', type=str, required=True, help="Directory containing images")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the images")
    args = parser.parse_args()
    process_dir_images(args.source_dir, args.output_dir)


if __name__ == "__main__":
    main()
