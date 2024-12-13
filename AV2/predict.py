import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
from PIL import Image, ImageTk, ImageDraw

def predict_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        results = model.predict(source=file_path, show=False, save=False, show_conf=False)
        original_img = Image.open(file_path)
        original_width, original_height = original_img.size
        img = original_img.resize((500, 500))
        draw = ImageDraw.Draw(img)
        
        termite_names = {
            0: "Coptotermes Gestroi (Cupim Subterrâneo Asiático)",
            1: "Cryptotermes Brevis (Cupim de Madeira Seca)",
            2: "Nasutitermes Corniger (Cupim Arbóreo)"
        }
        
        termite_info = {
            0: "Distribuição: Originalmente nativo do sudeste asiático, mas invasivo em várias partes do mundo, incluindo o Brasil.\n"
               "Habitat: Vive em colônias subterrâneas, mas pode construir ninhos em madeira úmida ou estruturas de edifícios.\n"
               "Dieta: Madeira e materiais celulósicos (papel, papelão, tecidos).\n"
               "Estragos: Causa danos significativos em estruturas de madeira, fiações e móveis; é considerado uma das espécies mais destrutivas de cupins.",
            1: "Distribuição: Originário das regiões tropicais das Américas; atualmente encontrado em muitos países devido ao transporte humano.\n"
               "Habitat: Vive dentro de peças de madeira seca (móveis, vigas, pisos).\n"
               "Dieta: Exclusivamente madeira, preferindo peças secas e bem acabadas.\n"
               "Estragos: Fura galerias internas em madeiras, comprometendo móveis e estruturas; deixa resíduos (grânulos fecais) visíveis.",
            2: "Distribuição: América do Sul e Central, com maior incidência em regiões tropicais.\n"
               "Habitat: Constrói ninhos visíveis em árvores, postes, e até em construções humanas.\n"
               "Dieta: Madeira, material celulósico, e até gramíneas.\n"
               "Estragos: Menos agressivo em relação a estruturas urbanas; preferem árvores e madeira externa."
        }
        
        detected_termites = set()
        detected_info = {}
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                class_id = int(box.cls.item())
                detected_termites.add(termite_names[class_id])
                if class_id not in detected_info:
                    detected_info[class_id] = termite_info[class_id]
                
                # Adjust coordinates to match resized image
                x1 = x1 * 500 / original_width
                y1 = y1 * 500 / original_height
                x2 = x2 * 500 / original_width
                y2 = y2 * 500 / original_height
                
                draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        
        img = ImageTk.PhotoImage(img)
        panel.config(image=img)
        panel.image = img
        
        if detected_termites:
            result_label.config(text="Cupim detectado: " + ", ".join(detected_termites) + "\n\n" + "\n\n".join(detected_info.values()))
        else:
            result_label.config(text="Nenhum cupim detectado.")

model = YOLO('yolo11m_train27.pt')

root = tk.Tk()
root.title("Detector de Cupins")
root.geometry("600x800")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

panel = tk.Label(frame, bg="#f0f0f0")
panel.pack(pady=10)

btn = tk.Button(frame, text="Selecionar Imagem", command=predict_image, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
btn.pack(pady=10)

result_label = tk.Label(frame, text="", wraplength=500, justify="left", bg="#f0f0f0", font=("Arial", 10))
result_label.pack(pady=10)

root.mainloop()