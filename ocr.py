import os
from typing import Dict, List

def _google_vision(paths: List[str]) -> Dict[str, str]:
    try:
        from google.cloud import vision
    except Exception:
        return {}
    creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds or not os.path.isfile(creds):
        return {}
    client = vision.ImageAnnotatorClient()
    out: Dict[str, str] = {}
    for p in paths:
        try:
            with open(p, 'rb') as f:
                content = f.read()
            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            if response.error.message:
                out[p] = ''
                continue
            annotations = response.text_annotations
            text = annotations[0].description if annotations else ''
            out[p] = text
        except Exception:
            out[p] = ''
    return out

def _tesseract(paths: List[str]) -> Dict[str, str]:
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        return {}
    out: Dict[str, str] = {}
    for p in paths:
        try:
            img = Image.open(p)
            text = pytesseract.image_to_string(img)
            out[p] = text
        except Exception:
            out[p] = ''
    return out

def extract_texts(paths: List[str]):
    data = _google_vision(paths)
    if data or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        return data, 'vision'
    data2 = _tesseract(paths)
    if data2:
        return data2, 'tesseract'
    return {}, ''