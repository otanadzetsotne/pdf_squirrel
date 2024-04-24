import os
import argparse
from tqdm import tqdm
from pdf2image import convert_from_path


def pdf_to_images(source_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_filenames = os.listdir(source_dir)
    pdf_filenames = list(filter(lambda x: x.endswith('.pdf'), pdf_filenames))

    # List all PDF files in the source directory
    for i_pdf, filename in enumerate(pdf_filenames):
        if filename.endswith('.pdf'):
            # Construct the full path to the PDF file
            pdf_path = os.path.join(source_dir, filename)

            # Convert PDF to a list of images
            images = convert_from_path(pdf_path, dpi=300, fmt='jpeg')

            # Save each page as an image
            for i_img, image in tqdm(
                    enumerate(images),
                    desc=f'Processing {filename} {i_pdf}/{len(pdf_filenames)}',
                    total=len(images),
            ):
                image_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_page_{i_img + 1}.jpg')
                if not os.path.exists(image_path):
                    image.save(image_path, 'JPEG')

    print("Conversion completed.")


def main():
    parser = argparse.ArgumentParser(description="Convert PDF files to images")
    parser.add_argument('--source_dir', type=str, required=True, help="Directory containing PDF files")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the images")
    args = parser.parse_args()
    pdf_to_images(args.source_dir, args.output_dir)


if __name__ == "__main__":
    main()
