import os
import argparse
from functools import partial
from concurrent.futures import ProcessPoolExecutor

from PIL import Image, ImageFilter


def blur_text_blocks(image_path, output_path, box_blur_radius=5):
    """
    Applies a blur effect to the text blocks on a document image to visually separate them.

    Args:
        image_path (LiteralString | str | bytes): Path to the source image file.
        output_path (LiteralString | str | bytes): Path to the file to save the processed image.
        box_blur_radius (int): The radius of the Gaussian blur.

    Returns:
        bool: True if processing and saving were successful, otherwise False.
    """
    try:
        image = Image.open(image_path)
        image = image.filter(ImageFilter.BoxBlur(box_blur_radius))
        image = image.filter(ImageFilter.GaussianBlur(5))
        image.save(output_path)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def process_proxy(image, src, dest, box_blur_radius):
    """
    Helper function to process each image by specifying source and destination paths.
    """
    src_path = os.path.join(src, image)
    dest_path = os.path.join(dest, image)
    return blur_text_blocks(src_path, dest_path, box_blur_radius)


def process_dir_images(source_dir, output_dir, box_blur_radius):
    """
    Processes all images in a directory and saves them to another directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    process = partial(process_proxy, src=source_dir, dest=output_dir, box_blur_radius=box_blur_radius)
    images = os.listdir(source_dir)

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
        results = pool.map(process, images)
        list(results)  # Evaluate the map to wait for all processes to complete


def main():
    """
    Main function to parse arguments and call the processing function.
    """
    parser = argparse.ArgumentParser(description="Blur text blocks on images for visual separation")
    parser.add_argument('--source_dir', type=str, required=True, help="Directory containing images")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the blurred images")
    parser.add_argument('--box_blur_radius', type=int, default=20, help="Radius of the Gaussian blur")
    args = parser.parse_args()

    process_dir_images(args.source_dir, args.output_dir, args.box_blur_radius)


if __name__ == "__main__":
    main()
