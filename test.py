import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# tesseract 安裝位置 (which tesseract 取得)
tesseract_path = '/opt/homebrew/bin/tesseract'

# 圖片路徑
image_path = 'original/hjlv.png'
#image_path = 'after_depoint.jpg'

class OCR():
    """OCR
    圖片驗證碼識別
    """    
    def __init__(self, tesseract_path):
        # 請下  which tesseract 取得 tesseract 安裝位置，並更新至此
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def generateAllFilterImages(self, image_path):
        # 讀取圖片
        img = Image.open(image_path)

        # 灰階
        img = img.convert('L')

        # 提高對比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)

        # 給予遮罩
        filters = [
            None,
            ImageFilter.BLUR,
            ImageFilter.CONTOUR,
            ImageFilter.DETAIL,
            ImageFilter.EDGE_ENHANCE,
            ImageFilter.EDGE_ENHANCE_MORE,
            ImageFilter.EMBOSS,
            ImageFilter.FIND_EDGES,
            ImageFilter.SHARPEN,
            ImageFilter.SMOOTH,
            ImageFilter.SMOOTH_MORE,
        ]

        filter_names = [
            'None',
            'BLUR',
            'CONTOUR',
            'DETAIL',
            'EDGE_ENHANCE',
            'EDGE_ENHANCE_MORE',
            'EMBOSS',
            'FIND_EDGES',
            'SHARPEN',
            'SMOOTH',
            'SMOOTH_MORE',
        ]

        for index, current_filter in enumerate(filters):
            # 給予遮罩
            if current_filter is not None:
                filtered_img = img.filter(current_filter)
            else:
                filtered_img = img.copy()

            # 儲存處理過的圖片
            suffix = filter_names[index]
            self.saveModifiedImage(filtered_img, image_path, suffix)
        

    def run(self, image_path):
        # 產生處理過的目標檔案 (套上各種 Filter)
        self.generateAllFilterImages(image_path)

        # Loop modified 資料夾
        for root, _dir, file in  os.walk('./modified'):
            for filename in file:
                if filename.endswith('.png'):
                    # 設定 Tesseract 只識別小寫英文字母
                    custom_config = r'--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz'
                    # 執行 OCR，並 Log 出結果
                    text = pytesseract.image_to_string(file, config=custom_config)
                    base_file_name, _ = os.path.splitext(os.path.basename(image_path))
                    print(f'檔名: {base_file_name}, 結果: {text}\n')

    # 保存處理過的圖片，儲存至 modified 資料夾，使用原始檔案名稱
    def saveModifiedImage(self, img, image_path, suffix):
        modified_folder_path = 'modified'
        base_file_name, file_extension = os.path.splitext(os.path.basename(image_path))
        
        # 建立檔案名稱 hjlv-None.png
        modified_file_name = f"{base_file_name}-{suffix}{file_extension}"
        
        # 建立完整檔案路徑 modified/hjlv-None.png
        modified_image_path = os.path.join(modified_folder_path, modified_file_name)

        # 儲存圖片
        img.save(modified_image_path)

if __name__ == "__main__":
    # 先執行產生 多種 Filter 檔案
    TEST = OCR(tesseract_path)
    TEST.run(image_path)

    # Loop modified 資料夾進行判斷
    for root, _dir, file in  os.walk('./modified'):
        for filename in file:
            if filename.endswith('.png'):
                # 檔案位置
                image_path = f'modified/{filename}'

                # 設定 Tesseract 只識別小寫英文字母
                custom_config = r'--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz'

                # 執行 OCR，並 Log 出結果
                text = pytesseract.image_to_string(image_path, config=custom_config)
                
                print(f'檔名: {filename}, 結果: {text}\n')