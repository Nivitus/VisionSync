# ai_backend/model/model_utils.py

import torch
from PIL import Image, ImageDraw, ImageFont
import os

def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()
    return model

def process_image(model, image_file, output_filename):
    with Image.open(image_file) as img:
        image = img.convert('RGB')
    
    results = model(image)
    
    detections = []
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 48)  
    except IOError:
        font = ImageFont.load_default()

    for *xyxy, conf, cls in results.xyxy[0]:
        label = f"{results.names[int(cls)]} {conf:.2f}"
        box = [float(x) for x in xyxy]
        detections.append({
            'class': results.names[int(cls)],
            'confidence': float(conf),
            'bbox': box
        })
        
        draw.rectangle(box, outline="red", width=5) 
        left, top, right, bottom = font.getbbox(label)
        text_width = right - left
        text_height = bottom - top
        text_position = (box[0], max(0, box[1] - text_height - 5))
        
        draw.rectangle([text_position[0], text_position[1], 
                        text_position[0] + text_width, text_position[1] + text_height], 
                       fill="red")
        
        draw.text(text_position, label, fill="white", font=font)

    image.save(os.path.join('outputs', output_filename), format='JPEG')
    
    return {
        'detections': detections
    }