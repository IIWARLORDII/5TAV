import os
import cv2
import torch
from yolov8 import YOLOv8

# /e:/5TAV/AV2/av2.py


# Configurações do projeto
IMAGE_DIR = 'images'
MODEL_PATH = 'models/yolov8_model.pth'
LABELS = ['species1', 'species2', 'species3']  # Substitua pelos nomes reais das espécies

# Função para carregar o modelo
def load_model(model_path):
    model = YOLOv8(model_path)
    return model

# Função para realizar a detecção
def detect_species(image_path, model):
    image = cv2.imread(image_path)
    results = model.predict(image)
    return results

# Função principal
def main():
    # Verifica se o diretório de imagens existe
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    # Carrega o modelo
    model = load_model(MODEL_PATH)
    
    # Itera sobre as imagens no diretório
    for image_name in os.listdir(IMAGE_DIR):
        image_path = os.path.join(IMAGE_DIR, image_name)
        results = detect_species(image_path, model)
        print(f"Resultados para {image_name}: {results}")

if __name__ == "__main__":
    main()