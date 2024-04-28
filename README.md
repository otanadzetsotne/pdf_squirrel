# Pdf Squirrel

## Overview
The Pdf Squirrel project is designed to facilitate the detection and manipulation of graphical and text blocks in images. This repository includes scripts for finding blocks in images, converting PDF files to images, normalizing and processing document images, applying blurs to specific sections, and drawing rectangles around detected sentences in images.

## Features
- **Block Detection**: Identify and outline blocks in images.
- **PDF to Image Conversion**: Convert PDF documents into images.
- **Image Normalization**: Process images to enhance text visibility and remove graphical elements.
- **Blur Effects**: Apply blur effects to text blocks to visually separate them.
- **Sentence Detection**: Draw rectangles around detected text sentences.

## Installation
Clone the repository and navigate to the directory:
```bash
git clone https://github.com/yourusername/pdf_squirrel.git
cd pdf_squirrel
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Each script in the repository can be run independently, depending on the task. Below are examples of how to use each script:

### Finding Blocks
```bash
python find_blocks.py --source_dir=path_to_images --output_dir=path_to_save_images
```
### Converting PDFs to Images
```
python pdf_to_img.py --source_dir=path_to_pdfs --output_dir=path_to_save_images
```

### Normalizing Images
```
python img_normalize.py --source_dir=path_to_images --output_dir=path_to_save_images
```

### Applying Blur to Text Blocks
```
python img_blur.py --source_dir=path_to_images --output_dir=path_to_save_images --box_blur_radius=5
```

### Drawing Rectangles Around Sentences
```
python sentence_blocks.py --source_dir=path_to_images --output_dir=path_to_save_images
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or create an issue if you have suggestions or find a bug.

## License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
