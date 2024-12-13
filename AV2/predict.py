import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
from PIL import Image, ImageTk, ImageDraw

def predict_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        results = model.predict(source=file_path, show=False, save=False, show_conf=False)
        img = Image.open(file_path)
        draw = ImageDraw.Draw(img)
        
        termite_names = {
            0: "Coptotermes Gestroi (Cupim Subterrâneo Asiático)",
            1: "Cryptotermes Brevis (Cupim de Madeira Seca)",
            2: "Nasutitermes Corniger (Cupim Arbóreo)"
        }
        
        detected_termites = set()
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                class_id = int(box.cls.item())
                detected_termites.add(termite_names[class_id])
                draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        
        img = ImageTk.PhotoImage(img)
        panel.config(image=img)
        panel.image = img
        
        if detected_termites:
            result_label.config(text="Cupim detectado: " + ", ".join(detected_termites))
        else:
            result_label.config(text="Nenhum cupim detectado.")

model = YOLO('yolo11m_train27.pt')

root = tk.Tk()
root.title("Detector de Cupins")
root.geometry("600x800")

frame = tk.Frame(root)
frame.pack()

panel = tk.Label(frame)
panel.pack()

btn = tk.Button(frame, text="Selecionar Imagem", command=predict_image)
btn.pack()

result_label = tk.Label(frame, text="")
result_label.pack()

root.mainloop()