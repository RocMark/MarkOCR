import os
from ocr import OCR
import pytesseract
from PIL import Image

code_img = 'storage/hjlv.png'
tesseract_path = '/opt/homebrew/bin/tesseract'
ocr = OCR(tesseract_path)

for root, _dir, file in  os.walk('./storage'):
    for filename in file:
        if filename.endswith('.png'):
            text = ocr.convert(os.path.join(root, filename))
            result = filename.split('.')[0]
            print(f'text: {text}, result: {result}')