# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 21:32:46 2025

@author: Mete
"""

import os
import random
import shutil
import xml.etree.ElementTree as ET

# 1. Ayarlar
images_folder = 'C:/Users/Mete/Desktop/dataset/ZD001_FD_IG/ZD001_FD_IG/ZD001_FD_IG/images2'  # Resimlerin olduğu klasör
xml_folder = 'C:/Users/Mete/Desktop/dataset/ZD001_FD_IG/ZD001_FD_IG/ZD001_FD_IG/labels'     # XML dosyalarının olduğu klasör
output_folder = 'C:/Users/Mete/Desktop/fabric_dataset' # Çıkış klasörü

classes = ['BrokenEnd']  # Sınıf isimleri burada, gerekirse listeye yeni sınıf eklenir
train_ratio = 0.8        # Eğitim için %80 kullan

# 2. Yardımcı Fonksiyonlar
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_path, txt_path):
    in_file = open(xml_path)
    tree = ET.parse(in_file)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(txt_path, 'w') as out_file:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")

# 3. Dataset Klasör Yapısı Kuruluyor
for folder in ['train/images', 'train/labels', 'val/images', 'val/labels']:
    os.makedirs(os.path.join(output_folder, folder), exist_ok=True)

# 4. Fotoğrafları Listele
image_files = [f for f in os.listdir(images_folder) if f.endswith('.jpg') or f.endswith('.png')]

# 5. Train / Val Bölme
random.shuffle(image_files)
split_idx = int(len(image_files) * train_ratio)
train_files = image_files[:split_idx]
val_files = image_files[split_idx:]

# 6. İşlem Başlat
def process_files(file_list, mode='train'):
    for image_file in file_list:
        name, ext = os.path.splitext(image_file)
        xml_file = name + '.xml'

        # Kopyala
        shutil.copy(os.path.join(images_folder, image_file), os.path.join(output_folder, f'{mode}/images', image_file))

        # Label Dönüştür
        xml_path = os.path.join(xml_folder, xml_file)
        txt_path = os.path.join(output_folder, f'{mode}/labels', name + '.txt')

        if os.path.exists(xml_path):
            convert_annotation(xml_path, txt_path)

process_files(train_files, mode='train')
process_files(val_files, mode='val')

print("✅ Tüm veri seti YOLO formatına dönüştürüldü ve bölündü.")
print(f"Toplam: {len(image_files)} görüntü")
print(f"Train: {len(train_files)} görüntü")
print(f"Validation: {len(val_files)} görüntü")
