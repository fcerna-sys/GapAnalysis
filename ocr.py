import os
import base64
from typing import Dict, List
import multiprocessing
import io

SAFE_IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}

def _is_safe_image_path(p: str) -> bool:
    try:
        ext = os.path.splitext(p)[1].lower()
        if ext not in SAFE_IMAGE_EXTS:
            return False
        if not os.path.isfile(p):
            return False
        return True
    except Exception:
        return False

def _qwen2_vl(paths: List[str]) -> Dict[str, str]:
    """
    Extrae texto de imágenes usando Qwen2 VL 7B Instruct a través de la API REST de LM Studio.
    El endpoint por defecto es http://localhost:1234/v1/chat/completions
    """
    out: Dict[str, str] = {}
    
    try:
        import requests
        from PIL import Image
    except ImportError:
        return {}
    
    # Obtener el endpoint de LM Studio desde variables de entorno o usar el predeterminado
    lm_studio_endpoint = os.environ.get('LM_STUDIO_ENDPOINT', 'http://localhost:1234/v1/chat/completions')
    
    prompt = "Extract all text visible in this image. Return only the text content, nothing else. If there is no text, return an empty string."
    
    for p in paths:
        try:
            # Validar que el archivo existe y es una imagen válida
            if not _is_safe_image_path(p):
                out[p] = ''
                continue
            
            # Optimizar imagen antes de enviar (redimensionar si es muy grande)
            try:
                img = Image.open(p).convert('RGB')
                # Redimensionar si es muy grande (máx 2048px para OCR)
                max_size = 2048
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Comprimir a JPEG
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=90, optimize=True)
                output.seek(0)
                image_data = output.read()
            except Exception:
                # Fallback: leer imagen original
                with open(p, 'rb') as f:
                    image_data = f.read()
            
            # Convertir a base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Determinar el tipo MIME de la imagen
            img_ext = os.path.splitext(p)[1].lower()
            mime_type = 'image/jpeg'
            if img_ext == '.png':
                mime_type = 'image/png'
            elif img_ext == '.webp':
                mime_type = 'image/webp'
            elif img_ext == '.gif':
                mime_type = 'image/gif'
            
            # Obtener el nombre del modelo desde variables de entorno o usar el predeterminado
            model_name = os.environ.get('LM_STUDIO_MODEL', 'qwen2-vl-7b-instruct')
            
            # Preparar el payload para la API de LM Studio (formato compatible con OpenAI)
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                "max_tokens": 512,
                "temperature": 0.1
            }
            
            # Hacer la petición a la API de LM Studio
            response = requests.post(
                lm_studio_endpoint,
                json=payload,
                timeout=60  # Timeout de 60 segundos
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extraer el texto de la respuesta
                if 'choices' in result and len(result['choices']) > 0:
                    text = result['choices'][0].get('message', {}).get('content', '').strip()
                    out[p] = text
                else:
                    out[p] = ''
            else:
                # Si falla la petición, intentar sin el formato de imagen (fallback)
                # Algunas versiones de LM Studio pueden requerir un formato diferente
                try:
                    # Formato alternativo para modelos de visión
                    model_name = os.environ.get('LM_STUDIO_MODEL', 'qwen2-vl-7b-instruct')
                    payload_alt = {
                        "model": model_name,
                        "messages": [
                            {
                                "role": "user",
                                "content": f"{prompt}\n\n[Imagen: {os.path.basename(p)}]"
                            }
                        ],
                        "max_tokens": 512,
                        "temperature": 0.1
                    }
                    response_alt = requests.post(
                        lm_studio_endpoint,
                        json=payload_alt,
                        timeout=60
                    )
                    if response_alt.status_code == 200:
                        result_alt = response_alt.json()
                        if 'choices' in result_alt and len(result_alt['choices']) > 0:
                            text = result_alt['choices'][0].get('message', {}).get('content', '').strip()
                            out[p] = text
                        else:
                            out[p] = ''
                    else:
                        out[p] = ''
                except Exception:
                    out[p] = ''
        except Exception:
            out[p] = ''
    
    return out

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

def _tesseract_worker(path: str, conn):
    try:
        import pytesseract
        from PIL import Image
        if not _is_safe_image_path(path):
            conn.send('')
            return
        # Opcional: respetar ruta de Tesseract desde entorno
        try:
            cmd = os.environ.get('TESSERACT_CMD')
            if cmd and os.path.isfile(cmd):
                import pytesseract as _pt
                _pt.pytesseract.tesseract_cmd = cmd
        except Exception:
            pass
        img = Image.open(path).convert('RGB')
        max_size = 2048
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        # Usar config conservadora
        try:
            text = pytesseract.image_to_string(img, config='--psm 6')
        except Exception:
            text = ''
        conn.send(text or '')
    except Exception:
        try:
            conn.send('')
        except Exception:
            pass

def _tesseract(paths: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for p in paths:
        try:
            parent_conn, child_conn = multiprocessing.Pipe()
            proc = multiprocessing.Process(target=_tesseract_worker, args=(p, child_conn))
            proc.daemon = True
            proc.start()
            # Timeout estricto para evitar bloqueos
            if parent_conn.poll(10):
                text = parent_conn.recv()
                out[p] = text
            else:
                try:
                    proc.terminate()
                except Exception:
                    pass
                out[p] = ''
        except Exception:
            out[p] = ''
    return out

def extract_texts(paths: List[str]):
    """
    Extrae texto de imágenes usando el siguiente orden de prioridad:
    1. Google Vision (si hay credenciales en .env)
    2. Qwen2 VL 7B Instruct (si no hay credenciales de Google Vision)
    3. Tesseract (fallback final)
    """
    # Verificar si hay credenciales de Google Vision
    creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    has_google_creds = creds and os.path.isfile(creds)
    
    # Si hay credenciales de Google Vision, usarlas
    if has_google_creds:
        data = _google_vision(paths)
        if data:
            return data, 'vision'
        # Si Google Vision falla pero hay credenciales, retornar vacío con 'vision'
        return data, 'vision'
    
    # Si no hay credenciales de Google Vision, usar Qwen2 VL
    data_qwen = _qwen2_vl(paths)
    if data_qwen:
        return data_qwen, 'qwen2-vl'
    
    # Fallback a Tesseract
    data2 = _tesseract(paths)
    if data2:
        return data2, 'tesseract'
    
    return {}, ''
