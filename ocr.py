import pytesseract, cv2

def extract_text_from_image(path):
    img = cv2.imread(path)
    return pytesseract.image_to_string(img)